CREATE DATABASE evaluation_system;
USE evaluation_system;

DROP TABLE IF EXISTS Persons;
CREATE TABLE Persons(
	IdPerson INT NOT NULL AUTO_INCREMENT,
	Name VARCHAR(512),

	PRIMARY KEY(IdPerson)
);

DROP TABLE IF EXISTS Quizzes;
CREATE TABLE Quizzes(
	IdQuiz INT NOT NULL AUTO_INCREMENT,
	Name VARCHAR(512),
    Description TEXT,

	PRIMARY KEY(IdQuiz)
);

DROP TABLE IF EXISTS Questions;
CREATE TABLE Questions(
	IdQuestion INT NOT NULL AUTO_INCREMENT,
    IdQuiz INT,
    Description TEXT,

	PRIMARY KEY(IdQuestion),
    CONSTRAINT Questions_IdQuiz_FK FOREIGN KEY(IdQuiz) REFERENCES Quizzes(IdQuiz) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Answers;
CREATE TABLE Answers(
	IdAnswer INT NOT NULL AUTO_INCREMENT,
    IdQuestion INT,
    Description TEXT,
    Correct BOOLEAN,

	PRIMARY KEY(IdAnswer),
    CONSTRAINT Answers_IdQuestion_FK FOREIGN KEY(IdQuestion) REFERENCES Questions(IdQuestion) ON DELETE CASCADE
);

DROP TABLE IF EXISTS PersonsQuizzes;
CREATE TABLE PersonsQuizzes(
	IdPersonQuiz INT NOT NULL AUTO_INCREMENT,
    IdPerson INT,
    IdQuiz INT,

	PRIMARY KEY(IdPersonQuiz),
    CONSTRAINT PersonsQuizzes_IdPerson_FK FOREIGN KEY(IdPerson) REFERENCES Persons(IdPerson) ON DELETE CASCADE,
    CONSTRAINT PersonsQuizzes_IdQuiz_FK FOREIGN KEY(IdQuiz) REFERENCES Quizzes(IdQuiz) ON DELETE CASCADE
);

DROP TABLE IF EXISTS PersonsAnwers;
CREATE TABLE PersonsAnwers(
	IdPersonAnswer INT NOT NULL AUTO_INCREMENT,
    IdPerson INT,
    IdAnswer INT,

	PRIMARY KEY(IdPersonAnswer),
    CONSTRAINT PersonsAnwers_IdPerson_FK FOREIGN KEY(IdPerson) REFERENCES Persons(IdPerson) ON DELETE CASCADE,
    CONSTRAINT PersonsAnwers_IdAnswer_FK FOREIGN KEY(IdAnswer) REFERENCES Answers(IdAnswer) ON DELETE CASCADE
);

