import os
c = open('w:/VS/IoscXAWS-Project/frontend/js/pages/dashboard2.js', encoding='utf-8').read()
c = c.replace('console.log(Student Data:, student);', 'console.log(\"Student Data:\", student);')
c = c.replace('console.log(Calculated pcent:, pcent);', 'console.log(\"Calculated pcent:\", pcent);')
open('w:/VS/IoscXAWS-Project/frontend/js/pages/dashboard2.js', 'w', encoding='utf-8').write(c)
