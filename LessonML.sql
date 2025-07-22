-- ===================================
-- USERS TABLE
-- ===================================
CREATE TABLE Users (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    Email NVARCHAR(255) UNIQUE NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(50) CHECK (Role IN ('student', 'teacher', 'admin')) NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);

-- ===================================
-- COURSES TABLE
-- ===================================
CREATE TABLE Courses (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Description NVARCHAR(MAX),
    Level NVARCHAR(50), -- Beginner, Intermediate, Advanced
    CreatedAt DATETIME DEFAULT GETDATE()
);

-- ===================================
-- LESSONS TABLE
-- ===================================
CREATE TABLE Lessons (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CourseId INT NOT NULL,
    Title NVARCHAR(255) NOT NULL,
    Content NVARCHAR(MAX),
    LessonOrder INT,
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (CourseId) REFERENCES Courses(Id)
);

-- ===================================
-- ENROLLMENTS TABLE
-- ===================================
CREATE TABLE Enrollments (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    CourseId INT NOT NULL,
    EnrolledAt DATETIME DEFAULT GETDATE(),
    Progress FLOAT DEFAULT 0,
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (CourseId) REFERENCES Courses(Id)
);

-- ===================================
-- QUIZ_ATTEMPTS TABLE
-- ===================================
CREATE TABLE QuizAttempts (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    LessonId INT NOT NULL,
    UserId INT NOT NULL,
    Score FLOAT DEFAULT 0,
    AttemptedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (LessonId) REFERENCES Lessons(Id),
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

-- ===================================
-- (Optional) SUBMISSIONS TABLE - nếu cần nộp bài tự luận
-- ===================================
CREATE TABLE Submissions (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    LessonId INT NOT NULL,
    UserId INT NOT NULL,
    Content NVARCHAR(MAX),
    Grade FLOAT,
    SubmittedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (LessonId) REFERENCES Lessons(Id),
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);


-- ===================================
-- Insert USERS
-- ===================================
INSERT INTO Users (Name, Email, PasswordHash, Role)
VALUES 
(N'Nguyen Van A', 'a@example.com', 'hash1', 'student'),
(N'Tran Thi B', 'b@example.com', 'hash2', 'student'),
(N'Le Van C', 'c@example.com', 'hash3', 'student'),
(N'Pham Thi D', 'd@example.com', 'hash4', 'student'),
(N'Do Van E', 'e@example.com', 'hash5', 'student'),
(N'Nguyen Thi F', 'f@example.com', 'hash6', 'teacher'),
(N'Hoang Van G', 'g@example.com', 'hash7', 'teacher'),
(N'Admin User', 'admin@example.com', 'hashadmin', 'admin'),
(N'Nguyen Van H', 'h@example.com', 'hash8', 'student'),
(N'Pham Thi I', 'i@example.com', 'hash9', 'student');

-- ===================================
-- Insert COURSES
-- ===================================
INSERT INTO Courses (Title, Description, Level)
VALUES
(N'English Beginner', N'Basic English for starters.', 'Beginner'),
(N'Business English', N'English for business communication.', 'Intermediate'),
(N'IELTS Preparation', N'Prepare for the IELTS test.', 'Advanced');

-- ===================================
-- Insert LESSONS
-- CourseId will be 1, 2, 3
-- ===================================
INSERT INTO Lessons (CourseId, Title, Content, LessonOrder)
VALUES
(1, N'Unit 1: Greetings', N'Hello, Hi, Good morning', 1),
(1, N'Unit 2: Numbers', N'One, Two, Three', 2),
(1, N'Unit 3: Days and Months', N'Monday, January...', 3),
(1, N'Unit 4: Family', N'Father, Mother...', 4),
(1, N'Unit 5: Food', N'Breakfast, Lunch...', 5),

(2, N'Unit 1: Meetings', N'Business meetings vocabulary', 1),
(2, N'Unit 2: Emails', N'Writing effective emails', 2),
(2, N'Unit 3: Presentations', N'Giving presentations', 3),
(2, N'Unit 4: Negotiation', N'Negotiation terms', 4),

(3, N'Unit 1: Listening Skills', N'IELTS Listening practice', 1),
(3, N'Unit 2: Reading Skills', N'IELTS Reading practice', 2),
(3, N'Unit 3: Writing Task 1', N'IELTS Writing Task 1', 3),
(3, N'Unit 4: Writing Task 2', N'IELTS Writing Task 2', 4),
(3, N'Unit 5: Speaking Skills', N'IELTS Speaking practice', 5);

-- ===================================
-- Insert ENROLLMENTS
-- Random students enroll various courses
-- ===================================
INSERT INTO Enrollments (UserId, CourseId, Progress)
VALUES
(1, 1, 20.0),
(1, 2, 0.0),
(2, 1, 50.0),
(3, 1, 80.0),
(3, 3, 10.0),
(4, 2, 30.0),
(5, 2, 90.0),
(5, 3, 60.0),
(9, 1, 40.0),
(10, 3, 70.0);

-- ===================================
-- Insert QUIZ_ATTEMPTS
-- Random scores for lessons
-- ===================================
-- ✅ FIX QuizAttempts
INSERT INTO QuizAttempts (LessonId, UserId, Score)
VALUES
(1, 1, 80),
(2, 1, 60),
(3, 1, 70),
(1, 2, 90),
(2, 2, 85),
(3, 2, 88),
(4, 3, 65),
(5, 3, 75),
(6, 4, 50),
(7, 4, 55),
(8, 5, 95),
(9, 5, 88),
(10, 5, 92),
(11, 3, 40),
(12, 3, 35),
(13, 10, 70),
(14, 10, 72);

-- ✅ FIX Submissions
INSERT INTO Submissions (LessonId, UserId, Content, Grade)
VALUES
(1, 1, N'Hello teacher, this is my greeting assignment.', 85),
(2, 1, N'Numbers homework.', 75),
(6, 4, N'Meeting minutes submission.', 65),
(11, 3, N'Listening practice essay.', 55),
(14, 10, N'Speaking practice recording.', 80);



-- ================================================
-- 1) Drop all FOREIGN KEY constraints
-- ================================================
DECLARE @sql NVARCHAR(MAX) = '';

SELECT @sql += '
ALTER TABLE [' + SCHEMA_NAME(t.schema_id) + '].[' + t.name + '] DROP CONSTRAINT [' + fk.name + '];'
FROM sys.foreign_keys fk
JOIN sys.tables t ON fk.parent_object_id = t.object_id;

EXEC sp_executesql @sql;

-- ================================================
-- 2) Drop all tables
-- ================================================
SET @sql = '';

SELECT @sql += '
DROP TABLE [' + SCHEMA_NAME(schema_id) + '].[' + name + '];'
FROM sys.tables;

EXEC sp_executesql @sql;




-- ===================================
-- USER_ACTIONS TABLE
-- Log hành vi nhỏ để training RL / RecSys
-- ===================================
CREATE TABLE UserActions (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    LessonId INT,
    Action NVARCHAR(255) NOT NULL, -- start_lesson, finish_lesson, skip_lesson, view_hint, etc.
    Metadata NVARCHAR(MAX), -- JSON: {"duration": 120, "device": "mobile"}
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (LessonId) REFERENCES Lessons(Id)
);

-- ===================================
-- USER_LESSON_QVALUES TABLE
-- Lưu Q-value cho RL (hoặc bạn có thể coi như user_weight)
-- ===================================
CREATE TABLE UserLessonQValues (
    UserId INT NOT NULL,
    LessonId INT NOT NULL,
    QValue FLOAT DEFAULT 0,
    LastUpdated DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (UserId, LessonId),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (LessonId) REFERENCES Lessons(Id)
);

-- ===================================
-- RL_MODELS TABLE (OPTIONAL)
-- Nếu bạn dùng Deep RL và cần versioning cho model
-- ===================================
CREATE TABLE RLModels (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Version NVARCHAR(50) NOT NULL,
    FilePath NVARCHAR(255) NOT NULL, -- link S3/MinIO hoặc local path
    CreatedAt DATETIME DEFAULT GETDATE(),
    Note NVARCHAR(MAX)
);

-- ===================================
-- USER_EMBEDDINGS TABLE (OPTIONAL)
-- Nếu bạn làm Collaborative Filtering / RecSys
-- Lưu vector latent của user
-- ===================================
CREATE TABLE UserEmbeddings (
    UserId INT PRIMARY KEY,
    Embedding VARBINARY(MAX), -- hoặc NVARCHAR(MAX) nếu encode base64
    UpdatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

-- ===================================
-- LESSON_EMBEDDINGS TABLE (OPTIONAL)
-- Vector latent cho bài học (nếu làm Item-Based RecSys)
-- ===================================
CREATE TABLE LessonEmbeddings (
    LessonId INT PRIMARY KEY,
    Embedding VARBINARY(MAX),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (LessonId) REFERENCES Lessons(Id)
);

INSERT INTO UserActions (UserId, LessonId, Action, Metadata)
VALUES
(1, 1, 'start_lesson', N'{"duration": 120, "device": "mobile"}'),
(1, 1, 'finish_lesson', N'{"duration": 300, "device": "mobile"}'),
(2, 2, 'start_lesson', N'{"duration": 90, "device": "web"}'),
(2, 2, 'view_hint', N'{"hint_type": "grammar"}'),
(3, 3, 'skip_lesson', N'{"reason": "too easy"}'),
(4, 4, 'start_lesson', N'{"duration": 150, "device": "tablet"}'),
(5, 5, 'finish_lesson', N'{"duration": 400, "device": "web"}');


INSERT INTO UserLessonQValues (UserId, LessonId, QValue)
VALUES
(1, 1, 0.8),
(1, 2, 0.6),
(2, 1, 0.7),
(2, 3, 0.5),
(3, 4, 0.4),
(4, 5, 0.9),
(5, 6, 0.3);


INSERT INTO RLModels (Version, FilePath, Note)
VALUES
('v1.0', '/models/rl/v1.0/model.bin', N'Initial baseline model'),
('v1.1', '/models/rl/v1.1/model.bin', N'Improved reward shaping'),
('v2.0', '/models/rl/v2.0/model.bin', N'Deep RL with attention');


INSERT INTO UserEmbeddings (UserId, Embedding)
VALUES
(1, CAST('0x1234567890ABCDEF' AS VARBINARY(MAX))),
(2, CAST('0xABCDEF1234567890' AS VARBINARY(MAX))),
(3, CAST('0xFEDCBA0987654321' AS VARBINARY(MAX)));
