# Generative AI API
Set of generative ai services in python deployed in kubernetes.

- **video-generation:** Text to video generation using potat1 model.
- **text-generation:** Text generation using Falcon-7b.
- **object-generation:** 3D object generation from text using openai open source shap-e.
- **music-generation:** Music generator using META model audiocraft
- **image-generation:** Image generation using stable diffusion 2.1
- **document-qna-hf:** Document question and answer using, langchain and huggingfaces models.
- **document-qna-cohere:** Document question and answer using, langchain and cohere AI.

## Configuration

### Create OKE cluster
Manually create an OKE cluster, with one CPU nodepool and add a second nodepool of GPUs, myself I use four T100 to deploy all the services. Make sure to add suficient disk space to these machines, because some of the images are 40 GB in size.

### ENV variables
Set variables so you can run all the configuration.

- Region OCIR, check for [region-key](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryprerequisites.htm#Availab)
- Tenancy name
- User id


```bash
export REGION_OCIR='<region-key>.ocir.io'
export TENANCY_NAME='<tenancy-name>'
export USER_ID='<user-id>'
```

### Secret creation
Its necesary to create three keys to deploy all the services.

- A secret to OCIR (oracle registry).
- A secret to Huggingface Hub API KEY. (singup into huggingface and create a READ token)
- A secret for Cohere AI. (signup and use the default their API key)

```bash
# OCIR secret
kubectl create secret docker-registry ocirsecret --docker-server=$REGION_OCIR --docker-username="$TENANCY_NAME/$USER_ID" --docker-password='<password>' --docker-email=$USER_ID

# Huggingface secret
kubectl create secret generic huggingfacehub-api-token --from-literal=HUGGINGFACEHUB_API_TOKEN=hf_token

# Cohere secret
kubectl create secret generic cohere-api-key --from-literal=COHERE_API_KEY=cohere_api_key
```

## Build
Login to OCIR, build each image and push them to OCIR.

```bash
docker login $REGION_OCIR --username $TENANCY_NAME/$USER_ID

cd object-generation
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/object-generation:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/object-generation:0.0.1

cd music-generation
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/music-generation:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/music-generation:0.0.1

cd video-generation
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/video-generation:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/video-generation:0.0.1

cd text-generation
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/text-generation:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/text-generation:0.0.1

cd image-generation
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/image-generation:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/image-generation:0.0.1

cd document-qna-hf
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/document-qna-hf:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/document-qna-hf:0.0.1

cd document-qna-cohere
docker build -t $REGION_OCIR/$TENANCY_NAME/generative-api/document-qna-cohere:0.0.1 .
docker push $REGION_OCIR/$TENANCY_NAME/generative-api/document-qna-cohere:0.0.1
```

## Manifest deploy
Apply the manifest you go individually applying each manifest or using the complete one.
```bash
kubectl apply -f manifest.yaml
```

## Testing
For testing you need to be inside the private subnet of the cluster an run curl using the service url given by each app. 
```bash
    kubectl get svc
```

Change the localhost for each cluster ip you get for each service.
```bash

# image-generation
curl -H "Content-Type: application/json" -d '{"prompt" : "bear with glasses"}' http://localhost:3000/generate_image -o image.png

# music-generation
curl -H "Content-Type: application/json" -d '{"prompt" : "bebop jazz", "duration": 8}' http://localhost:3000/generate_music -o temp.wav

# text-generation
curl -H "Content-Type: application/json" -d '{"prompt" : "what is the answer to life the universe and everything? response: ", "max_length": 200}' http://localhost:3000/generate_text

# video-generation
curl -H "Content-Type: application/json" -d '{"prompt" : "waterfall", "negative_prompt": "text, watermark, copyright, blurry, low resolution, blur, low quality", "width": 512, "height": 288, "num_steps": 25, "guidance_scale": 23,  "fps": 24, "num_frames":10 }' http://localhost:3000/generate_video -o temp.mp4

# object-generation
curl -H "Content-Type: application/json" -d '{"prompt" : "a shark", "return_type": "zip"}' http://localhost:3000/generate_3d_object -o 3d.zip


# document-qna-hf, supposing you have a file called state_of_the_union.txt
curl -F 'document=@state_of_the_union.txt' -F 'index=state_of_the_union' http://localhost:3000/load_file
curl http://localhost:3000/query_docs -H 'Content-Type: application/json'  -d '{"question": "What did the president say about Ketanji Brown Jackson?", "index":"state_of_the_union"}'

# document-qna-cohere, supposing you have a file called state_of_the_union.txt
curl -F 'document=@state_of_the_union.txt' -F 'index=state_of_the_union' http://localhost:3000/load_file
curl http://localhost:3000/query_docs -H 'Content-Type: application/json'  -d '{"question": "What did the president say about Ketanji Brown Jackson?", "index":"state_of_the_union"}'
```
