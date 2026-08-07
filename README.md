Food App WIP

Save, Read, and Commit to creating all your favorite recipes from popular influencers on Instagram, Tiktok, and more!


Requirements:
1. Node.js
2. Virtual Environment
3. Run pip install -r requirements.txt

Updating db:

flask --app run.py db upgrade

---

__Wanna test the api without a GUI? Use curl!__ 

(Pearl apparently is a better gui focused tester but curl is installed on almsot anything)

curl.exe -i -X POST `
    -H "Content-Type: application/json" `
    -d '{\"email\":\"curl-test@gmail.com\",\"name\":\"curl\",\"password\":\"curl\"}' `
    http://127.0.0.1:5000/signup

Powershell uses invoke, so this is the command for it. 'cleaner' than the forcing curl above and avoiding all the syntax parsing issues

Invoke-RestMethod -Uri "http://127.0.0.1:5000/signup" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"email":"curl-test@gmail.com","name":"curl","password":"curl"}'

Invoke-RestMethod -Uri "http://127.0.0.1:5000/recipes-submit" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"title":"test","source_url":"test.com","source_platform":"test", "ingredients":"test egg", "instructions":"step test", "image_url":"test.jpg", "submitted_by":"test"}'