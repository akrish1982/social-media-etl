-- database/init.sql
CREATE TABLE IF NOT EXISTS social_media_metrics (
    platform VARCHAR(50),
    timestamp BIGINT,
    engagement INT,
    likes INT,
    shares INT,
    comments INT
);