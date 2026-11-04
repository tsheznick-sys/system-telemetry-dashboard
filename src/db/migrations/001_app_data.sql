CREATE TABLE IF NOT EXISTS tasks (
  id text PRIMARY KEY,
  user_id text NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title varchar(100) NOT NULL,
  description varchar(500) NOT NULL DEFAULT '',
  priority varchar(10) NOT NULL CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
  status varchar(12) NOT NULL CHECK (status IN ('todo', 'in-progress', 'done')),
  category varchar(32) NOT NULL DEFAULT '',
  due_date date,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS tasks_user_updated_idx ON tasks (user_id, updated_at DESC);

CREATE TABLE IF NOT EXISTS user_settings (
  user_id text PRIMARY KEY REFERENCES "user"(id) ON DELETE CASCADE,
  thresholds jsonb NOT NULL DEFAULT '{"cpu":85,"memory":85,"errors":1}'::jsonb,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS telemetry_samples (
  id bigserial PRIMARY KEY,
  user_id text NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  recorded_at timestamptz NOT NULL,
  cpu_usage double precision NOT NULL,
  memory_usage double precision NOT NULL,
  active_connections integer NOT NULL,
  error_rate double precision NOT NULL,
  active_node text NOT NULL
);

CREATE INDEX IF NOT EXISTS telemetry_user_recorded_idx
  ON telemetry_samples (user_id, recorded_at DESC);
CREATE INDEX IF NOT EXISTS telemetry_recorded_retention_idx ON telemetry_samples (recorded_at);

CREATE TABLE IF NOT EXISTS system_events (
  id text PRIMARY KEY,
  user_id text NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  level varchar(10) NOT NULL CHECK (level IN ('INFO', 'WARN', 'SUCCESS', 'DEBUG')),
  message varchar(500) NOT NULL,
  occurred_at timestamptz NOT NULL
);

CREATE INDEX IF NOT EXISTS system_events_user_occurred_idx
  ON system_events (user_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS system_events_occurred_retention_idx ON system_events (occurred_at);

CREATE TABLE IF NOT EXISTS audit_events (
  id bigserial PRIMARY KEY,
  user_id text NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  action varchar(80) NOT NULL,
  resource_type varchar(40) NOT NULL,
  resource_id text,
  details jsonb NOT NULL DEFAULT '{}'::jsonb,
  occurred_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS audit_user_occurred_idx ON audit_events (user_id, occurred_at DESC);

CREATE OR REPLACE FUNCTION reject_audit_event_mutation()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF pg_trigger_depth() > 1 THEN
    RETURN OLD;
  END IF;
  RAISE EXCEPTION 'audit_events is append-only';
END;
$$;

DROP TRIGGER IF EXISTS audit_events_immutable ON audit_events;
CREATE TRIGGER audit_events_immutable
  BEFORE UPDATE OR DELETE ON audit_events
  FOR EACH ROW EXECUTE FUNCTION reject_audit_event_mutation();
