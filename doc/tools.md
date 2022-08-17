# Tools and Frameworks

## SAM (Serverless Application Model)

- A framework for building serverless applications on AWS.
- Provides a CLI to initialise, build and deploy applications.
- Provides a template that leverages Cloudformation for declaring and mnaaging applied changes to resources.

### Initialising a Lambda Project

``` bash
  sam init --name energy --runtime python3.9 --package-type Zip \   
           --architecture x86_64  --base-image amazon/python3.9 \
           --tracing --dependency-manager pip
```
