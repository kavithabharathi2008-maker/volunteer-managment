-- MySQL Database Schema for Community Needs Intelligence & Volunteer Matching

CREATE DATABASE IF NOT EXISTS community_db;
USE community_db;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'NGO', 'Volunteer', 'Admin'
    location VARCHAR(100),
    password_hash VARCHAR(128)
);

-- Issues Table
CREATE TABLE issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'Health', 'Food', 'Education', etc.
    urgency INT NOT NULL, -- 1 to 5
    description TEXT NOT NULL,
    date_reported DATETIME DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    reported_by_id INT,
    FOREIGN KEY (reported_by_id) REFERENCES users(id)
);

-- Volunteers Table
CREATE TABLE volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    skills VARCHAR(200) NOT NULL,
    availability VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tasks Table
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    volunteer_id INT,
    status VARCHAR(20) DEFAULT 'Pending', -- 'Pending', 'In Progress', 'Completed'
    priority_score INT DEFAULT 0,
    FOREIGN KEY (issue_id) REFERENCES issues(id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id)
);
