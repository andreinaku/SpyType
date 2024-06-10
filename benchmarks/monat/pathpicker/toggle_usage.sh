if grep "^if \_\_name\_\_" processInput.py; then
    sed -e '/if \_\_name\_\_/,+100 s/^/# /'  -i processInput.py;
    sed -e '/if \_\_name\_\_/,+100 s/^# //'  -i choose.py;
else
    sed -e '/if \_\_name\_\_/,+100 s/^/# /'  -i choose.py;
    sed -e '/if \_\_name\_\_/,+100 s/^# //'  -i processInput.py;
fi
