import sqlite3

conn = sqlite3.connect('bkr_database.db')
cursor = conn.cursor()

cursor.execute('SELECT id, title, date, location, time, status FROM health_camps')
camps = cursor.fetchall()

print('=' * 80)
print('Health Camps in Database:')
print('=' * 80)

if camps:
    for row in camps:
        print(f'ID: {row[0]}')
        print(f'Title: {row[1]}')
        print(f'Date: {row[2]}')
        print(f'Location: {row[3]}')
        print(f'Time: {row[4]}')
        print(f'Status: {row[5]}')
        print('-' * 80)
else:
    print('No health camps found in database!')

print(f'\nTotal camps: {len(camps)}')
conn.close()
