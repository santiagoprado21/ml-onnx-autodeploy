# Comandos para subir el proyecto a GitHub

## Paso 1: Verificar estado actual
```bash
git status
git branch
```

## Paso 2: Asegurarte de tener todos los cambios en master/main
```bash
git add .
git commit -m "Sistema completo de despliegue automático ML"
git push origin master
```

Si tu rama principal es "main" en vez de "master", usa:
```bash
git push origin main
```

## Paso 3: Subir a la rama dev
```bash
git checkout dev
git merge master
git push origin dev
```

Si tu rama principal es "main":
```bash
git checkout dev
git merge main
git push origin dev
```

## Paso 4: Subir a la rama prod
```bash
git checkout prod
git merge master
git push origin prod
```

Si tu rama principal es "main":
```bash
git checkout prod
git merge main
git push origin prod
```

## Paso 5: Volver a la rama principal
```bash
git checkout master
```

O si usas main:
```bash
git checkout main
```

## Verificar que todo se subió
Ve a tu repositorio en GitHub y verifica que:
- Existen 3 ramas: master (o main), dev, prod
- Cada rama tiene todos los archivos
- El archivo .github/workflows/test-and-deploy.yml está presente

## Si hay conflictos
Si git te dice que hay conflictos al hacer merge:
```bash
git merge --strategy-option theirs master
```

Esto acepta todos los cambios de master.

