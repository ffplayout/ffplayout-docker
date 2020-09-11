### Run:
-   `docker build --tag ffplayout-api:master .`
-   ```
    docker run --name ffplayout-api -p 8001:8001 \
    --volume /etc/ffplayout/ffplayout.yml:/etc/ffplayout/ffplayout.yml \
    --volume /var/log/logs:/var/log/ffplayout \
    --volume /tv-media:/tv-media \
    --volume /playlists:/playlists \
    -itd ffplayout-api:master
    ```

Default credentials are:
- User: admin
- pass: admin

Change this after build! In fontend or in ffplayout-api admin panel: http://localhost:8001/admin
