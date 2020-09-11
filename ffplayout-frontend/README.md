For testing change *localhost* from: `"API_URL='http://localhost:8001'"` to your *host IP* in the **Dockerfile**

### Run:
-   `docker build --tag ffplayout-frontend:master .`
-   ```
    docker run --name ffplayout-frontend -p 8088:80 -itd ffplayout-frontend:master
    ```

Default credentials are:
- User: admin
- pass: admin

Change this after build!
