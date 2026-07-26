@echo off
cd /d %~dp0
npx @11ty/eleventy --serve --port=8081
