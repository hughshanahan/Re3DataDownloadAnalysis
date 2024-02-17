curl -o t.xml https://www.re3data.org/api/v1/repositories
grep "\<id\>" t.xml | sed 's/\<id\>//' | sed 's/\<\/id\>//' > repos.txt
