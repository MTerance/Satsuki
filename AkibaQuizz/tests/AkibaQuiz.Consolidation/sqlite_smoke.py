"""Tests SQLite isolés, sans accès aux données utilisateur ni .NET.
Exécuter avec: python tests/sqlite_smoke.py
"""
from pathlib import Path
import re
import sqlite3

HERE = Path(__file__).resolve().parent
def source_root():
    for base in (HERE, *HERE.parents):
        if (base/'patch/AkibaQuiz.Infrastructure').exists():
            return base/'patch'
        if (base/'AkibaQuiz.Infrastructure').exists():
            return base
    raise AssertionError('Repository Game introuvable')
ROOT = source_root()
conn = sqlite3.connect(':memory:')
conn.executescript((HERE / 'schema.sql').read_text('utf-8'))
conn.execute('PRAGMA foreign_keys=ON')
assert conn.execute('PRAGMA foreign_keys').fetchone()[0] == 1

conn.execute("INSERT INTO Categories(Id,Name) VALUES(1,'Anime')")
conn.execute("INSERT INTO Tags(Id,Name,Color) VALUES(1,'Test','#ffff00')")
conn.execute("INSERT INTO TypeMedia(Id,Name) VALUES(1,'Image')")
conn.execute("INSERT INTO Medias(Id,Filename,IdTypeMedia) VALUES(1,'image.png',1)")
conn.execute("INSERT INTO QuestionsAnswers(Id,Question,Answer,IdCategory,CreationDate,LastUpdateDate,Author) VALUES(8,'Studio ?','Sunrise',1,'now','now','test')")
conn.execute("INSERT INTO QCMQuestion(Id,Question,CreationDate,LastUpdatedTDate,Author,IdCategory) VALUES(7,'Entreprises ?','now','now','test',1)")
conn.executemany("INSERT INTO QCMAnswer(Id,Answer) VALUES(?,?)", [(11, 'Sunrise'), (12, 'Sega')])
conn.executemany("INSERT INTO QCMQuizz(Id,IdQCMQuestion,IdQCMAnswer,IsTrue) VALUES(?,?,?,?)", [(31,7,11,'TRUE'), (32,7,12,'FALSE')])
conn.execute('INSERT INTO TagQuizz(IdTag,IdQCM) VALUES(1,7)')
conn.execute("INSERT INTO MediaQuizz(IdQCMQuestion,IdMedia,TypeDisplay) VALUES(7,1,'BeforeQuestion')")
conn.execute("INSERT INTO Games(Id,Name,Author,CreationDate) VALUES(1,'Game Test','admin','now')")
conn.executemany("INSERT INTO GameRounds(Id,Position,IdGame) VALUES(?,?,?)", [(20,1,1), (21,2,1)])
conn.executemany("INSERT INTO RoundQuestions(Id,Position,IdGameRound,IdQuestionAnswer,IdQCMQuestion) VALUES(?,?,?,?,?)", [(101,1,20,None,7), (102,2,20,8,None), (103,1,21,None,7)])

# Exécute la requête de catalogue extraite directement du repository C#.
source = (ROOT / 'AkibaQuiz.Infrastructure/Repositories/GameRepository.cs').read_text('utf-8')
match = re.search(r'const string sql\s*=\s*"""\s*(.*?)\s*"""\s*;', source, re.S)
assert match is not None, 'Requête catalogue introuvable'
summary = conn.execute(match.group(1)).fetchone()
assert summary == (1, 'Game Test', 2, 3), summary

question = conn.execute("SELECT q.Question,c.Name FROM QuestionsAnswers q JOIN Categories c ON c.Id=q.IdCategory WHERE q.Id=?", (8,)).fetchone()
assert question == ('Studio ?', 'Anime'), question
answers = conn.execute("SELECT l.Id,l.IdQCMAnswer,a.Answer,l.IsTrue FROM QCMQuizz l JOIN QCMAnswer a ON a.Id=l.IdQCMAnswer WHERE l.IdQCMQuestion=? ORDER BY l.Id", (7,)).fetchall()
assert [x[3] for x in answers] == ['TRUE','FALSE'], answers
linked_media = conn.execute("SELECT l.Id,l.IdMedia,m.Filename,m.IdTypeMedia,tm.Name AS TypeMediaName,l.TypeDisplay FROM MediaQuizz l JOIN Medias m ON m.Id=l.IdMedia JOIN TypeMedia tm ON tm.Id=m.IdTypeMedia WHERE l.IdQCMQuestion=?", (7,)).fetchone()
assert linked_media[2] == 'image.png', linked_media

try:
    conn.execute('DELETE FROM QCMQuestion WHERE Id=7')
    raise AssertionError('Une suppression FK aurait dû échouer')
except sqlite3.IntegrityError:
    pass

fk_errors = conn.execute('PRAGMA foreign_key_check').fetchall()
assert not fk_errors, fk_errors
print('SQLITE SMOKE PASS: catalogue, modèles, associations, FK; aucune base réelle modifiée.')
