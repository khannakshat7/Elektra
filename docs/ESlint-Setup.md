## Documentation and script to setup and run eslint and then add prettier code 

  -  Install ESLint using npm or yarn:-
   ```npm install eslint --save-dev``` or ```yarn add eslint --dev```
  - Set up a configuration file, and the easiest way to do that is to use the --init flag:-
    ```npx eslint --init``` or ```yarn run eslint --init```
  - ```--init``` assumes you have a package.json file already.If you don't, make sure to run ```npm init``` or ```yarn init``` beforehand
  -  Run ESLint on any file or directory like this:-
      ```npx eslint yourfile.js``` or ```yarn run eslint yourfile.js```
  - After running ```eslint --init```, you'll have a .eslintrc.{js,yml,json} file in your directory.
    In it, you'll see some rules configured like this:-
     {
    "rules": {
        "semi": ["error", "always"],
        "quotes": ["error", "double"]
    }
} 

  - Your .eslintrc.{js,yml,json} configuration file will also include the line:-
     {
    "extends": "eslint:recommended"
} 
  
  -  In package.json, inside "scripts", add another script, ```"lint":"eslint '**/*.js' --ignore-pattern node_modules/"```
