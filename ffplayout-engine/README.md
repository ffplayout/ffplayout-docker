### Run:
- `docker build --tag ffplayout-engine:1.0 .`
-   ```
    docker run --name ffplayout-engine -p 5555:5555 -p 64233:64233 \
    --volume /etc/ffplayout/ffplayout.yml:/etc/ffplayout/ffplayout.yml \
    --volume /var/log/ffplayout:/var/log/ffplayout \
    --volume /tv-media:/tv-media \
    --volume /playlists:/playlists \
    -itd ffplayout-engine:1.0
    ```

**Don't push this image to any public registry! The image contains a none free ffmpeg version, which is not allow to redistribute!**

ffplayout-engine can be control over [control-engine.py](assets/control-engine.py) like:

```
./control-engine.py -m start  # or stop, restart, reload
```

This will be done later by ffplayout-api.
