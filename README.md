# session-archive
Create a file archive from a Session using Flywheel's Python SDK

### Example Usage
This Gear is built to take a Flywheel Session ID and create a dataset archive (.zip) of all files within the session.

```
# The config file must contain the Flywheel Session ID and user's API key
docker run -ti --rm \
    -v $(pwd)/output:/flywheel/v0/output \
    -v $(pwd)/config.json:/flywheel/v0/config.json \
    flywheel/session-archive
```

Below is an example of the config.json file contents passed to the Gear
```
{
  "config": {
    "session_id": "111b333de6f8900000000000",
    "api_key": "example.flywheel.io:abcdeFGHI123456789"
  }
}
```
