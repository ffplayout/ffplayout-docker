### Run:
- `docker build --tag ffplayout-engine:1.0 .`
-   ```
    docker run --name ffplayout-engine -p 5555:5555 \
    --volume /etc/ffplayout/ffplayout.yml:/etc/ffplayout/ffplayout.yml \
    --volume /var/log/ffplayout:/var/log/ffplayout \
    --volume /tv-media:/tv-media \
    --volume /playlists:/playlists \
    -itd ffplayout-engine:1.0
    ```
