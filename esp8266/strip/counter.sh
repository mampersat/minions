for (( ; ; ))
do
  for i in {1..1000}; do
    echo m$i
    ./send.sh m$i
    sleep 1
  done

  # ./send.sh cycle
  # sleep 5

done
