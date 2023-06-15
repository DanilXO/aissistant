## Init:

1. Create template:
   ```commandline
   pybabel extract ./src -o locales/base.pot
   ```
   
2. Add new locale:
   ```commandline
   pybabel init -l ru_RU -i locales/base.pot -d locales
   ```
   
3. Translate.

4. Compile: 
   ```commandline
   pybabel compile -d locales
   ```

## Update:

1. ```commandline
   pybabel extract ./src -o locales/base.pot
   ```
   
2. ```commandline
   pybabel update -i locales/base.pot -d locales
   ```