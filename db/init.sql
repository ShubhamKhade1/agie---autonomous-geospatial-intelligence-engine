-- AGIE: TimescaleDB Initialization Schema
-- Optimized for High-Resolution Geospatial Signals

-- Enable TimescaleDB and PostGIS extensions
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS postgis CASCADE;

-- 1. Signals Table (Raw Normalized Satellite Feeds)
-- Stores multivariate data points for each ROI coordinate / H3 index
CREATE TABLE IF NOT EXISTS signals (
    time        TIMESTAMPTZ       NOT NULL,
    roi_id      TEXT              NOT NULL,
    h3_index    TEXT              NOT NULL,
    variable    TEXT              NOT NULL, -- e.g., 'SST', 'NDVI', 'SAR_L7', 'AIS_PRESENCE'
    value       DOUBLE PRECISION  NOT NULL, -- Normalized 0.0 to 1.0
    source      TEXT              NOT NULL, -- e.g., 'NASA_MODIS', 'COPERNICUS_CMEMS'
    metadata    JSONB
);

-- Convert 'signals' into a hyper-table partitioned by time
SELECT create_hypertable('signals', 'time', if_not_exists => TRUE);

-- Index for fast spatial-temporal lookups
CREATE INDEX IF NOT EXISTS idx_signals_roi_h3 ON signals (roi_id, h3_index, time DESC);

-- 2. Anomalies Table (Calculated Scores & AI Synthesis)
-- Stores the final output from the Reasoning & Dialogue layers
CREATE TABLE IF NOT EXISTS anomalies (
    time                TIMESTAMPTZ       NOT NULL,
    roi_id              TEXT              NOT NULL,
    score               DOUBLE PRECISION  NOT NULL, -- 0-100 Weighted Priority Score
    magnitude           DOUBLE PRECISION  NOT NULL, -- Residual from STL Baseline
    trajectory          DOUBLE PRECISION  NOT NULL, -- Rolling persistence/trend
    synthesis_report    TEXT              NOT NULL, -- Gemini's AI Analysis
    convergent_evidence JSONB             NOT NULL, -- Multi-sensor verification data
    is_active           BOOLEAN           DEFAULT TRUE
);

-- Convert 'anomalies' into a hyper-table partitioned by time
SELECT create_hypertable('anomalies', 'time', if_not_exists => TRUE);

-- Index for dashboard active alerts
CREATE INDEX IF NOT EXISTS idx_anomalies_roi_active ON anomalies (roi_id, is_active, time DESC);

-- 3. ROI Baseline Cache (Phase A: Seasonal Rhythm)
-- Stores the learned STL seasonal components for rapid comparison
CREATE TABLE IF NOT EXISTS roi_baselines (
    roi_id      TEXT              NOT NULL,
    variable    TEXT              NOT NULL,
    season_day  INT               NOT NULL, -- 1-366 (Day of Year)
    avg_value   DOUBLE PRECISION  NOT NULL, -- Seasonal mean
    std_dev     DOUBLE PRECISION  NOT NULL, -- Historical variance
    PRIMARY KEY (roi_id, variable, season_day)
);

-- Initial Mock Data for Phase 1/2 visualization
-- (This would normally be populated by the Celery Workers)
INSERT INTO roi_baselines (roi_id, variable, season_day, avg_value, std_dev) 
VALUES ('india_west_coast', 'SST', 150, 0.65, 0.05) ON CONFLICT DO NOTHING;
