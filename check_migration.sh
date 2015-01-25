#!/bin/bash

# 로컬 DB 스키마와 Metadata(ORM 클래스)로부터 만들어진 스키마를 비교하여 출력합니다.
# 만약 migration이 정확하게 이루어져 있다면, 빈 결과를 출력할 것입니다.
# 현재, PostgreSQL 데이터베이스만 사용 가능합니다.

# 결과는 SQL 형태로, 현재 로컬 DB가 Metadata로부터 만들어진 스키마와 일치하기 위해 적용되어야 할 명령들입니다.

# PostgreSQL 덤프 비교를 위해 pg_dump와 apgdiff가 필요합니다.

# 2개의 인자가 필요합니다.
# 1) 로컬 DB 이름
# 2) 출력파일명

# 사용 예: ./check_migration.sh alps diff.sql
# (로컬 DB명은 'alps', 출력파일명은 'diff.sql'로 함.)


if [ $# -ge 2 ]; then
	TEMP_DB_NAME="temp_alps_schema"
	TEMP_DB_URL="postgresql:///"
	TEMP_DB_URL+=$TEMP_DB_NAME
	TEMP_DUMP_FILE_1="temp_dump_file_1.sql"
	TEMP_DUMP_FILE_2="temp_dump_file_2.sql"

	# Construct a DB from the metadata
	createdb $TEMP_DB_NAME -E utf8 -T postgres
	alps schema --database-url $TEMP_DB_URL

	# Stamp current revision on the DB.
	alps migration $TEMP_DB_URL "alembic stamp head"

	# Make dumps and compare.
	pg_dump -Oxs -f $TEMP_DUMP_FILE_1 $1
	pg_dump -Oxs -f $TEMP_DUMP_FILE_2 $TEMP_DB_NAME
	apgdiff $TEMP_DUMP_FILE_1 $TEMP_DUMP_FILE_2 > $2

	# Clear the temporary files and DB.
	rm $TEMP_DUMP_FILE_1
	rm $TEMP_DUMP_FILE_2
	dropdb $TEMP_DB_NAME
else
	echo "Require two arguments."
	echo "1) the name of a local PostgreSQL DB"
	echo "2) the name of an output file"
fi
