/// <reference types="node" />

export type KeyEncryptionAlgorithm =
  | 'http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p'
  | 'http://www.w3.org/2009/xmlenc11#rsa-oaep'
  | 'http://www.w3.org/2001/04/xmlenc#rsa-1_5';

export type EncryptionAlgorithm =
  | 'http://www.w3.org/2001/04/xmlenc#aes128-cbc'
  | 'http://www.w3.org/2001/04/xmlenc#aes256-cbc'
  | 'http://www.w3.org/2009/xmlenc11#aes128-gcm'
  | 'http://www.w3.org/2009/xmlenc11#aes256-gcm'
  | 'http://www.w3.org/2001/04/xmlenc#tripledes-cbc';

export type DigestName = 'sha1' | 'sha256' | 'sha512';

export type Mgf1DigestName = 'sha1' | 'sha224' | 'sha256' | 'sha384' | 'sha512';

export interface KeyInfoOptions {
  /** RSA public key (PEM) used to wrap the symmetric key. */
  rsa_pub: string | Buffer;
  /** X.509 certificate (PEM) emitted in the KeyInfo. */
  pem: string | Buffer;
  /** Defaults to `rsa-oaep-mgf1p`. */
  keyEncryptionAlgorithm?: KeyEncryptionAlgorithm | (string & {});
  /** OAEP message digest. Defaults to `sha1`. */
  keyEncryptionDigest?: DigestName | (string & {});
  /**
   * MGF1 digest, a short name or a full `xmlenc11#mgf1*` URI. Only valid with
   * `xmlenc11#rsa-oaep`; `rsa-oaep-mgf1p` always uses MGF1-SHA1. Defaults to `sha1`.
   */
  keyEncryptionMgf?: Mgf1DigestName | (string & {});
  /** OAEP label, as a Buffer or a base64 string. */
  keyEncryptionOaepParams?: Buffer | string;
  /** Refuse insecure key transport (RSA-1.5). Defaults to `true`. */
  disallowEncryptionWithInsecureAlgorithm?: boolean;
  /** Log a warning when an insecure algorithm is used. Defaults to `true`. */
  warnInsecureAlgorithm?: boolean;
}

export interface EncryptOptions extends KeyInfoOptions {
  encryptionAlgorithm: EncryptionAlgorithm | (string & {});
  /** Encoding of `content` when it is a string. Defaults to `utf8`. */
  input_encoding?: BufferEncoding;
  /** Refuse insecure algorithms (RSA-1.5, 3DES, AES-CBC). Defaults to `true`. */
  disallowEncryptionWithInsecureAlgorithm?: boolean;
}

export interface DecryptOptions {
  /** RSA private key (PEM) that unwraps the symmetric key. */
  key: string | Buffer;
  /** Refuse insecure algorithms (RSA-1.5, 3DES, AES-CBC). Defaults to `true`. */
  disallowDecryptionWithInsecureAlgorithm?: boolean;
  /** Log a warning when an insecure algorithm is used. Defaults to `true`. */
  warnInsecureAlgorithm?: boolean;
}

/**
 * A parsed XML document from any DOM implementation (e.g. `@xmldom/xmldom`).
 * Kept structural so consumers don't need `lib.dom`.
 */
export interface XmlDocument {
  documentElement: unknown;
}

export type Callback<T> = (err: Error | null, result?: T) => void;

/** Encrypt `content` into an `<xenc:EncryptedData>` element (as XML text). */
export function encrypt(content: string | Buffer, options: EncryptOptions, callback: Callback<string>): void;

/** Decrypt an `<xenc:EncryptedData>` element, given as XML text or a parsed document. */
export function decrypt(xml: string | XmlDocument, options: DecryptOptions, callback: Callback<string>): void;

/** Wrap `symmetricKey` and return the `<KeyInfo>` XML. */
export function encryptKeyInfo(symmetricKey: Buffer | string, options: KeyInfoOptions, callback: Callback<string>): void;

/** Unwrap the symmetric key from an `<EncryptedData>` (or bare `<KeyInfo>`) document. */
export function decryptKeyInfo(doc: string | XmlDocument, options: DecryptOptions): Buffer;
