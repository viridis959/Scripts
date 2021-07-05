if [ $# -ge 2 ]
then
  if [ -e "./$1.py" ]
  then
    python "$1".py "${@:2}"
  else
    echo "尚未有$1.py"
  fi
else
  echo "用法：./clawer.sh <action> <argv1> [<argv2>...]"
fi
