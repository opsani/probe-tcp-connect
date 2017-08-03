# probe-tcp-connect
The tcp-connect probe performs a simple socket connect health check.  It attempts to open a socket on component instances.

The tcp-connect probe supports the following actions:

* `service_up` (default) - try to open a socket and keep retrying until success or the action times out

This action supports the following arguments:

* `port` - port number (default `80`)
* `timeout` - operation timeout *per service instance*, in seconds (default `120`).  This is how long to keep retrying to open the socket (success).

## examples

Here are a few examples in the form of quality gates specified in a Skopos TED file (target environment descriptor).  Quality gates associate probe executions to one or more component images.  During application deployment Skopos executes the specified probes to assess components deployed with matching images.

```yaml
vars:
    elastic_port:  "9300"
    fluentd_port:  "24224"

quality_gates:
    elastic:
        images:
            - elasticsearch:*
        steps:

            # check elasticsearch TCP transport on port 9300
            - probe:
                image: opsani/probe-tcp-connect:v1
                label: "tcp-connect port ${elastic_port}"
                arguments: { port: "${elastic_port}" }

    fluent:
        images:
            - fluent/fluentd:*
        steps:

            # check Fluentd forward protocol listen port 24224
            - probe:
                image: opsani/probe-tcp-connect:v1
                label: "tcp-connect port ${fluentd_port}"
                arguments: { port: "${fluentd_port}" }
```
