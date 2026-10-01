const {defineConfig} = require('@playwright/test');
module.exports = defineConfig({testDir:'./app/tests', webServer:{command:'.venv/bin/python app/server.py',url:'http://127.0.0.1:8000',reuseExistingServer:false},use:{baseURL:'http://127.0.0.1:8000'},projects:[{name:'phone',use:{viewport:{width:390,height:844}}},{name:'desktop',use:{viewport:{width:1280,height:900}}}]});
