### Run:
-   `docker build --tag ffplayout-api:1.0 .`
-   ```
    docker run --name ffplayout-api -p 8001:8001 \
    --volume /etc/ffplayout/ffplayout.yml:/etc/ffplayout/ffplayout.yml \
    --volume /var/log/logs:/var/log/ffplayout \
    --volume /tv-media:/tv-media \
    --volume /playlists:/playlists \
    -itd ffplayout-api:1.0
    ```
