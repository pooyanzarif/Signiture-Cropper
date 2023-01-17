# Signiture-Cropper
This script designed to find a signiture in the file, crop and resize it to a standard size. It is used widely in Pargar an Iranian Enterprise Automation.
---
# Persian
سامانه اتوماسیون اداری "پرگار" نیاز دارد که امضاء کارکنان را در قالب استانداردی ذخیره نماید.
- ابعاد امضای 500 در 500  باشد.
- پس زمینه شفاف باشد.
- امضای به صورت کامل و در مرکز تصویر قرار بگیرد.
- با فرمت PNG ذخیره گردد.
قبلا این کار به صورت دستی انجام می پذیرفت . به کمک این اسکریپت تمام امضاها به صورت خام در دایرکتوری مبدا قرار داده شده و سپس با اجرای این اسکریپت همه آنها پردازش و در دایرکتوری مقصد قرار می گیرد.
برای راهنمایی استفاده از اسکریپت از سوییچ -h استفاده کنید.
```sh
C:\ kasra.py -h
> usage: kasra.py [-h] [-s SOURCE] [-d DESTINATION] [-v]
> 
> Prepare signitures in Pargar standards. Written by "Pooyan Zarif"
> 
> options:
>  -h, --help            show this help message and exit
>  -s SOURCE, --source SOURCE
>                        Enter Source directory. Default is "source"
>  -d DESTINATION, --destination DESTINATION
>                        Enter destination directory. Default is "destination"
>  -v, --verbose         verbose
```
# Example
Copy all images in a directory and rename it to D1
Create an empty directory and rename it to D2
```sh
kasra.py -s D1 -d D2
```
