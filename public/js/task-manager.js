import { downloadCsv } from './csv.js';

const taskStorageKey = 'pulse.tasks';
let tasks = [];
let editingTaskId = null;

try {
  const savedTasks = JSON.parse(localStorage.getItem(taskStorageKey) || '[]');
  if (Array.isArray(savedTasks)) {
    tasks = savedTasks
      .filter(
        (task) =>
          task &&
          typeof task.id === 'string' &&
          typeof task.title === 'string' &&
          ['todo', 'in-progress', 'done'].includes(task.status) &&
          ['low', 'normal', 'high', 'urgent'].includes(task.priority) &&
          (!task.dueDate ||
            (typeof task.dueDate === 'string' &&
              !Number.isNaN(Date.parse(`${task.dueDate}T00:00:00`)))),
      )
      .map((task) => ({
        ...task,
        description: typeof task.description === 'string' ? task.description : '',
        category: typeof task.category === 'string' ? task.category : '',
        dueDate: typeof task.dueDate === 'string' ? task.dueDate : '',
      }));
  }
} catch (error) {
  console.warn('Unable to load saved tasks:', error);
}

function persistTasks() {
  const storageStatus = document.getElementById('task-result-count');
  try {
    localStorage.setItem(taskStorageKey, JSON.stringify(tasks));
    storageStatus.textContent = `${tasks.filter((task) => task.status !== 'done').length} open · saved locally`;
    storageStatus.removeAttribute('data-error');
  } catch (error) {
    console.error('Unable to save tasks:', error);
    storageStatus.textContent = 'Could not save tasks in this browser';
    storageStatus.dataset.error = 'true';
    return false;
  }
  return true;
}

function renderTasks() {
  const query = document.getElementById('task-search').value.trim().toLocaleLowerCase();
  const priorityFilter = document.getElementById('task-priority-filter').value;
  const filtered = tasks.filter((task) => {
    const searchable =
      `${task.title} ${task.description || ''} ${task.category || ''}`.toLocaleLowerCase();
    return (
      (!query || searchable.includes(query)) &&
      (priorityFilter === 'all' || task.priority === priorityFilter)
    );
  });
  const lists = {
    todo: document.getElementById('todo-list'),
    'in-progress': document.getElementById('progress-list'),
    done: document.getElementById('done-list'),
  };
  const statusMeta = {
    todo: { count: 'todo-count', label: 'to do' },
    'in-progress': { count: 'progress-count', label: 'in progress' },
    done: { count: 'done-count', label: 'completed' },
  };
  const priorityLabels = { low: 'Low', normal: 'Normal', high: 'High', urgent: 'Urgent' };
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  for (const [taskStatus, list] of Object.entries(lists)) {
    const statusTasks = filtered
      .filter((task) => task.status === taskStatus)
      .sort((a, b) => {
        const priorityRank = { urgent: 0, high: 1, normal: 2, low: 3 };
        const priorityDifference = priorityRank[a.priority] - priorityRank[b.priority];
        if (priorityDifference !== 0) return priorityDifference;
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;
        return a.dueDate.localeCompare(b.dueDate);
      });
    document.getElementById(statusMeta[taskStatus].count).textContent = statusTasks.length;

    if (statusTasks.length === 0) {
      const empty = document.createElement('div');
      empty.className = 'task-empty';
      empty.textContent = tasks.length
        ? 'No matching tasks here.'
        : taskStatus === 'todo'
          ? 'Your queue is clear. Add a task to get started.'
          : 'Tasks will appear here as work moves through the queue.';
      if (!tasks.length && taskStatus === 'todo') {
        const addButton = document.createElement('button');
        addButton.className = 'action-button';
        addButton.type = 'button';
        addButton.dataset.action = 'new-task';
        addButton.style.marginTop = '10px';
        addButton.textContent = 'Create your first task';
        empty.append(document.createElement('br'), addButton);
      }
      list.replaceChildren(empty);
      continue;
    }

    list.replaceChildren(
      ...statusTasks.map((task) => {
        const card = document.createElement('article');
        card.className = `task-card${task.status === 'done' ? ' is-done' : ''}`;
        card.dataset.taskId = task.id;

        const top = document.createElement('div');
        top.className = 'task-card-top';
        const title = document.createElement('h3');
        title.className = 'task-title';
        title.textContent = task.title;

        const description = document.createElement('p');
        description.className = 'task-description';
        description.textContent = task.description || 'No description added.';

        const meta = document.createElement('div');
        meta.className = 'task-meta';
        const priority = document.createElement('span');
        priority.className = 'task-chip task-priority';
        priority.dataset.priority = task.priority;
        priority.textContent = priorityLabels[task.priority];
        meta.append(priority);
        if (task.category) {
          const category = document.createElement('span');
          category.className = 'task-chip';
          category.textContent = task.category;
          meta.append(category);
        }
        if (task.dueDate) {
          const due = document.createElement('time');
          due.className = 'task-due';
          due.dateTime = task.dueDate;
          const dueDate = new Date(`${task.dueDate}T00:00:00`);
          due.textContent = `Due ${dueDate.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}`;
          if (task.status !== 'done' && dueDate < today) due.classList.add('is-overdue');
          meta.append(due);
        }
        top.append(title);
        card.append(top, description, meta);

        const actions = document.createElement('div');
        actions.className = 'task-card-actions';
        const statusSelect = document.createElement('select');
        statusSelect.className = 'task-status-select';
        statusSelect.dataset.action = 'status';
        statusSelect.setAttribute('aria-label', `Change status for ${task.title}`);
        [
          ['todo', 'To do'],
          ['in-progress', 'In progress'],
          ['done', 'Completed'],
        ].forEach(([value, label]) => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = label;
          option.selected = value === task.status;
          statusSelect.append(option);
        });
        const actionGroup = document.createElement('div');
        actionGroup.className = 'task-action-group';
        const editButton = document.createElement('button');
        editButton.className = 'task-action';
        editButton.type = 'button';
        editButton.dataset.action = 'edit';
        editButton.setAttribute('aria-label', `Edit ${task.title}`);
        editButton.innerHTML =
          '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m14 5 5 5M4 20l4.3-.9L19 8.4a2.1 2.1 0 0 0-3-3L5.3 16.1 4 20Z" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
        const deleteButton = document.createElement('button');
        deleteButton.className = 'task-action';
        deleteButton.type = 'button';
        deleteButton.dataset.action = 'delete';
        deleteButton.setAttribute('aria-label', `Delete ${task.title}`);
        deleteButton.innerHTML =
          '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16m-10 4v6m4-6v6M6 7l1 14h10l1-14M9 7V4h6v3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
        actionGroup.append(editButton, deleteButton);
        actions.append(statusSelect, actionGroup);
        card.append(actions);
        return card;
      }),
    );
  }

  const todo = tasks.filter((task) => task.status === 'todo').length;
  const active = tasks.filter((task) => task.status === 'in-progress').length;
  const done = tasks.filter((task) => task.status === 'done').length;
  document.getElementById('task-total').firstChild.textContent = tasks.length;
  document.getElementById('task-todo').firstChild.textContent = todo;
  document.getElementById('task-active').firstChild.textContent = active;
  document.getElementById('task-done').firstChild.textContent = done;
  document.getElementById('nav-task-count').textContent = tasks.filter(
    (task) => task.status !== 'done',
  ).length;
  if (!document.getElementById('task-result-count').dataset.error) {
    document.getElementById('task-result-count').textContent =
      `${filtered.length} shown · ${tasks.length} total`;
  }
}

function showTaskForm(task) {
  const form = document.getElementById('task-form');
  editingTaskId = task?.id ?? null;
  form.reset();
  form.elements.title.value = task?.title ?? '';
  form.elements.description.value = task?.description ?? '';
  form.elements.priority.value = task?.priority ?? 'normal';
  form.elements.status.value = task?.status ?? 'todo';
  form.elements.category.value = task?.category ?? '';
  form.elements.dueDate.value = task?.dueDate ?? '';
  document.getElementById('task-dialog-title').textContent = editingTaskId
    ? 'Edit task'
    : 'Create task';
  document.getElementById('save-task-button').textContent = editingTaskId
    ? 'Save changes'
    : 'Create task';
  document.getElementById('task-dialog').showModal();
  form.elements.title.focus();
}

export function initializeTaskManager() {
  document.getElementById('new-task-button').addEventListener('click', () => showTaskForm());
  document.getElementById('close-task-dialog').addEventListener('click', () => {
    document.getElementById('task-dialog').close();
  });
  document.getElementById('cancel-task-dialog').addEventListener('click', () => {
    document.getElementById('task-dialog').close();
  });
  document.getElementById('task-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const form = document.getElementById('task-form');
    const formData = new FormData(form);
    const updatedTask = {
      id: editingTaskId ?? crypto.randomUUID(),
      title: String(formData.get('title') || '').trim(),
      description: String(formData.get('description') || '').trim(),
      priority: String(formData.get('priority')),
      status: String(formData.get('status')),
      category: String(formData.get('category') || '').trim(),
      dueDate: String(formData.get('dueDate') || ''),
    };
    if (!updatedTask.title) {
      form.elements.title.reportValidity();
      return;
    }

    if (editingTaskId) {
      tasks = tasks.map((task) => (task.id === editingTaskId ? updatedTask : task));
    } else {
      tasks.unshift(updatedTask);
    }
    persistTasks();
    renderTasks();
    document.getElementById('task-dialog').close();
  });
  document.getElementById('task-search').addEventListener('input', renderTasks);
  document.getElementById('task-priority-filter').addEventListener('change', renderTasks);

  const taskBoard = document.querySelector('.task-board');
  taskBoard.addEventListener('change', (event) => {
    const select = event.target.closest('select[data-action="status"]');
    if (!select) return;
    const card = select.closest('[data-task-id]');
    tasks = tasks.map((task) =>
      task.id === card.dataset.taskId ? { ...task, status: select.value } : task,
    );
    persistTasks();
    renderTasks();
  });
  taskBoard.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-action]');
    if (!button) return;
    if (button.dataset.action === 'new-task') {
      showTaskForm();
      return;
    }
    const card = button.closest('[data-task-id]');
    const task = tasks.find((item) => item.id === card?.dataset.taskId);
    if (!task) return;

    if (button.dataset.action === 'edit') {
      showTaskForm(task);
    } else if (button.dataset.action === 'delete' && window.confirm(`Delete “${task.title}”?`)) {
      tasks = tasks.filter((item) => item.id !== task.id);
      persistTasks();
      renderTasks();
    }
  });
  document.getElementById('export-tasks-button').addEventListener('click', () => {
    if (tasks.length === 0) {
      document.getElementById('task-result-count').textContent = 'There are no tasks to export';
      return;
    }
    downloadCsv(
      [
        ['title', 'description', 'priority', 'status', 'workstream', 'dueDate'],
        ...tasks.map((task) => [
          task.title,
          task.description,
          task.priority,
          task.status,
          task.category,
          task.dueDate,
        ]),
      ],
      'pulse-tasks.csv',
    );
  });
  renderTasks();
}
