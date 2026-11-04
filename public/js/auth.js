import { apiFetch } from './api.js';

const authScreen = document.getElementById('auth-screen');
const appShell = document.getElementById('app-shell');
const authForm = document.getElementById('auth-form');
const authNotice = document.getElementById('auth-notice');
const authModeButton = document.getElementById('auth-mode-toggle');
let mode = 'signin';
let googleEnabled = false;
let passwordResetEnabled = false;
let resetToken = '';

function showNotice(message, isError = true) {
  authNotice.textContent = message;
  authNotice.hidden = !message;
  authNotice.dataset.error = String(isError);
}

function setMode(nextMode) {
  mode = nextMode;
  const isSignup = mode === 'signup';
  const isSignin = mode === 'signin';
  const isCredentialMode = isSignin || isSignup;
  document.getElementById('auth-form').hidden = !isCredentialMode;
  document.getElementById('password-reset-request').hidden = mode !== 'forgot';
  document.getElementById('password-reset-form').hidden = mode !== 'reset';
  document.getElementById('auth-name-field').hidden = !isSignup;
  document.getElementById('auth-name').required = isSignup;
  document.getElementById('auth-submit').textContent = isSignup ? 'Create account' : 'Sign in';
  authModeButton.textContent = isSignup ? 'Already have an account? Sign in' : 'Create an account';
  document.getElementById('auth-heading').textContent =
    mode === 'signup'
      ? 'Create your workspace'
      : mode === 'forgot'
        ? 'Reset your password'
        : mode === 'reset'
          ? 'Choose a new password'
          : 'Welcome back';
  authModeButton.hidden = !isCredentialMode;
  document.getElementById('forgot-password-button').hidden = !isSignin || !passwordResetEnabled;
  document.getElementById('back-to-signin-button').hidden = isCredentialMode;
  document.getElementById('auth-divider').hidden = !isSignin;
  document.getElementById('google-signin').hidden = !isSignin || !googleEnabled;
  document.getElementById('sso-form').hidden = !isSignin;
  document.getElementById('auth-footnote').hidden = !isSignin;
  showNotice('');
}

async function showApplication(user) {
  authScreen.hidden = true;
  appShell.hidden = false;
  const initials = user.name
    .split(/\s+/)
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
  document.getElementById('operator-avatar').textContent = initials || 'OP';
  document.getElementById('operator-avatar').title = user.email;
  document.getElementById('operator-name').textContent = user.name;
  window.dispatchEvent(new CustomEvent('pulse:authenticated', { detail: { user } }));
  try {
    const capability = await apiFetch('/api/profile');
    document.getElementById('manage-sso-button').hidden = !capability.isAdmin;
  } catch (error) {
    console.error('Unable to load account profile:', error);
  }
}

async function initializeAuth() {
  const url = new URL(window.location.href);
  resetToken = url.searchParams.get('token') || '';
  if (resetToken) {
    authScreen.hidden = false;
    setMode('reset');
    return;
  }
  if (url.searchParams.get('error') === 'INVALID_TOKEN') {
    authScreen.hidden = false;
    setMode('signin');
    showNotice('This password reset link is invalid or expired. Request a new link.');
    return;
  }
  try {
    const [session, options] = await Promise.all([
      apiFetch('/api/auth/get-session'),
      apiFetch('/api/auth-options'),
    ]);
    googleEnabled = options.googleEnabled;
    passwordResetEnabled = options.passwordResetEnabled;
    setMode('signin');
    if (session?.user) {
      await showApplication(session.user);
      return;
    }
    authScreen.hidden = false;
  } catch (error) {
    authScreen.hidden = false;
    showNotice(`Unable to connect to the authentication service. ${error.message}`);
  }
}

authModeButton.addEventListener('click', () => setMode(mode === 'signin' ? 'signup' : 'signin'));
document.getElementById('forgot-password-button').addEventListener('click', () => {
  const email = authForm.elements.email.value;
  setMode('forgot');
  document.querySelector('#password-reset-request [name="email"]').value = email;
});
document.getElementById('back-to-signin-button').addEventListener('click', () => {
  resetToken = '';
  window.history.replaceState({}, '', window.location.pathname);
  setMode('signin');
});
authForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(authForm);
  const body = {
    email: String(formData.get('email')).trim(),
    password: String(formData.get('password')),
  };
  if (mode === 'signup') body.name = String(formData.get('name')).trim();
  const endpoint = mode === 'signup' ? '/api/auth/sign-up/email' : '/api/auth/sign-in/email';
  const button = document.getElementById('auth-submit');
  button.disabled = true;
  showNotice('');
  try {
    const response = await apiFetch(endpoint, {
      method: 'POST',
      body: JSON.stringify({ ...body, callbackURL: window.location.origin }),
    });
    if (mode === 'signup' && !response?.token) {
      setMode('signin');
      showNotice('If an account can be created, a verification email will be sent.', false);
      return;
    }
    if (!response?.user) {
      showNotice('Check your email for a verification link before signing in.', false);
      return;
    }
    authForm.reset();
    await showApplication(response.user);
  } catch (error) {
    showNotice(error.message);
  } finally {
    button.disabled = false;
  }
});

document.getElementById('password-reset-request').addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = String(new FormData(event.currentTarget).get('email')).trim();
  try {
    await apiFetch('/api/auth/request-password-reset', {
      method: 'POST',
      body: JSON.stringify({ email, redirectTo: window.location.origin }),
    });
    showNotice('If that address is registered, a password reset link has been sent.', false);
  } catch (error) {
    showNotice(error.message);
  }
});

document.getElementById('password-reset-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const newPassword = String(new FormData(event.currentTarget).get('password'));
  try {
    await apiFetch('/api/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ newPassword, token: resetToken }),
    });
    window.history.replaceState({}, '', window.location.pathname);
    resetToken = '';
    setMode('signin');
    showNotice('Your password has been updated. Sign in with your new password.', false);
  } catch (error) {
    showNotice(error.message);
  }
});

document.getElementById('google-signin').addEventListener('click', async () => {
  try {
    await apiFetch('/api/auth/sign-in/social', {
      method: 'POST',
      body: JSON.stringify({ provider: 'google', callbackURL: window.location.origin }),
    }).then((result) => {
      if (result.url) window.location.assign(result.url);
    });
  } catch (error) {
    showNotice(error.message);
  }
});

document.getElementById('sso-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = String(new FormData(event.currentTarget).get('email')).trim();
  try {
    const result = await apiFetch('/api/auth/sign-in/sso', {
      method: 'POST',
      body: JSON.stringify({ email, callbackURL: window.location.origin }),
    });
    if (result.url) window.location.assign(result.url);
  } catch (error) {
    showNotice(error.message);
  }
});

document.getElementById('signout-button').addEventListener('click', async () => {
  try {
    await apiFetch('/api/auth/sign-out', { method: 'POST', body: '{}' });
    window.location.reload();
  } catch (error) {
    console.error('Unable to sign out:', error);
  }
});
window.addEventListener('pulse:session-expired', () => window.location.reload());

const ssoDialog = document.getElementById('sso-dialog');
const ssoForm = document.getElementById('sso-form-dialog');
document.getElementById('manage-sso-button').addEventListener('click', () => ssoDialog.showModal());
document.getElementById('close-sso-dialog').addEventListener('click', () => ssoDialog.close());
document.getElementById('cancel-sso-dialog').addEventListener('click', () => ssoDialog.close());
document.getElementById('sso-type').addEventListener('change', (event) => {
  const isSaml = event.currentTarget.value === 'saml';
  document.getElementById('oidc-fields').hidden = isSaml;
  document.getElementById('saml-fields').hidden = !isSaml;
});
ssoForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const fields = new FormData(ssoForm);
  const type = String(fields.get('type'));
  const body = {
    type,
    providerId: String(fields.get('providerId')).trim(),
    issuer: String(fields.get('issuer')).trim(),
    domain: String(fields.get('domain')).trim(),
  };
  if (type === 'oidc') {
    body.oidcConfig = {
      clientId: String(fields.get('clientId')).trim(),
      clientSecret: String(fields.get('clientSecret')),
      discoveryEndpoint: String(fields.get('discoveryEndpoint')).trim(),
    };
  } else {
    body.samlConfig = {
      entryPoint: String(fields.get('entryPoint')).trim(),
      cert: String(fields.get('cert')).trim(),
      audience: String(fields.get('audience')).trim(),
    };
  }
  const notice = document.getElementById('sso-notice');
  notice.hidden = true;
  try {
    const registration = await apiFetch('/api/admin/sso/providers', {
      method: 'POST',
      body: JSON.stringify(body),
    });
    ssoForm.reset();
    ssoDialog.close();
    const statusDetail = document.getElementById('status-detail');
    statusDetail.replaceChildren(
      document.createTextNode(
        registration.type === 'saml'
          ? 'SAML provider registered. Service-provider metadata: '
          : `OIDC provider registered. Callback URL: ${registration.callbackUrl}`,
      ),
    );
    if (registration.metadataUrl) {
      const metadataUrl = new URL(registration.metadataUrl, window.location.origin);
      if (metadataUrl.origin === window.location.origin) {
        const link = document.createElement('a');
        link.href = metadataUrl;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = 'View SP metadata';
        statusDetail.append(link);
      }
    }
    window.dispatchEvent(new Event('pulse:audit-updated'));
  } catch (error) {
    notice.textContent = error.message;
    notice.dataset.error = 'true';
    notice.hidden = false;
  }
});

initializeAuth();
