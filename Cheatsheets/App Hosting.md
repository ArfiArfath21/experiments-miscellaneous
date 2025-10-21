To host your app on your personal domain and link it to the public IP of your Azure AKS service, you need to perform the following steps:

Steps to Host Your App on Your Domain

1. Acquire a Domain Name

	•	If you don’t already own a domain, purchase one from a domain registrar (e.g., GoDaddy, Namecheap, or Google Domains).

2. Map Your Domain to the Public IP

	•	Log in to your domain registrar’s control panel.
	•	Navigate to the DNS Management section.
	•	Create an A Record to map your domain or subdomain to the Azure public IP. For example:
	•	Host: @ or www (depending on whether you’re mapping the root domain or a subdomain)
	•	Type: A
	•	Value: 44.21.21.21 (your Azure public IP)
	•	TTL: Default (e.g., 3600 seconds)

3. Set Up an Ingress Controller in AKS

	•	If you haven’t already, deploy an ingress controller (like NGINX) to handle routing within your AKS cluster:
	•	Use the Helm chart for NGINX:

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx



4. Define an Ingress Resource

	•	Create a Kubernetes Ingress resource to define routing rules for your domain. Here’s an example YAML:

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-service-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: www.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80


	•	Apply the configuration:

kubectl apply -f ingress.yaml



5. Configure SSL/TLS for HTTPS (Optional but Recommended)

To serve your app over HTTPS, you need an SSL/TLS certificate.
	•	Option 1: Let’s Encrypt (Free)
	•	Use a tool like cert-manager to automatically issue and renew SSL certificates:
	1.	Install cert-manager:

kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml


	2.	Create a ClusterIssuer for Let’s Encrypt:

apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx


	3.	Update your Ingress resource to enable TLS:

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-service-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - www.yourdomain.com
    secretName: yourdomain-tls
  rules:
  - host: www.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80


	4.	Apply the updated Ingress:

kubectl apply -f ingress.yaml


	•	Option 2: Manually Obtain and Upload a Certificate
	•	Purchase or generate an SSL certificate.
	•	Store it as a Kubernetes secret:

kubectl create secret tls yourdomain-tls --cert=path-to-cert.pem --key=path-to-key.pem


	•	Reference this secret in your Ingress resource under the tls section.

6. Test Your Configuration

	•	Ensure the DNS records have propagated (this may take a few minutes to hours).
	•	Access your domain (http://www.yourdomain.com or https://www.yourdomain.com) and confirm that your app is accessible.

Summary of Requirements

	•	Domain DNS configured to point to the Azure public IP.
	•	AKS ingress controller set up for routing.
	•	Ingress resource created with domain-based rules.
	•	SSL/TLS certificates for HTTPS (optional but recommended).

Let me know if you’d like detailed commands for any specific step!

===
Yes, you can absolutely host your new deployment at a subdomain like https://abc.pqr.com/ while keeping your existing deployment on the root domain (https://www.pqr.com/). The steps to achieve this involve configuring DNS, ingress, and optionally SSL/TLS certificates for the subdomain. Here’s how you can set it up:

Steps to Host New Deployment at https://abc.pqr.com/

1. Set Up the Subdomain (abc.pqr.com)

	•	Go to your domain registrar’s DNS Management settings.
	•	Add a new A Record to map the subdomain to the same public IP of your AKS cluster (44.21.21.21):
	•	Host: abc
	•	Type: A
	•	Value: 44.21.21.21 (your Azure public IP)
	•	TTL: Default (e.g., 3600 seconds)

2. Update the Ingress Controller Configuration

	•	If your AKS cluster already has an ingress controller deployed (e.g., NGINX), update or create a new Ingress Resource to route traffic for abc.pqr.com.

Here’s an example YAML configuration for the new subdomain:

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: abc-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"  # Redirect HTTP to HTTPS
spec:
  tls:
  - hosts:
    - abc.pqr.com
    secretName: abc-pqr-tls  # Kubernetes Secret containing the SSL certificate
  rules:
  - host: abc.pqr.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: abc-service  # Name of your Kubernetes Service for the new deployment
            port:
              number: 80

	•	Replace abc-service with the name of the Kubernetes Service backing your new deployment.

Apply the configuration:

kubectl apply -f abc-ingress.yaml

3. Obtain an SSL/TLS Certificate for abc.pqr.com

To serve traffic over HTTPS, you need an SSL/TLS certificate for the subdomain.
	•	Option 1: Use Let’s Encrypt with cert-manager
	•	If cert-manager is installed in your cluster, request a new certificate for abc.pqr.com by creating a Certificate resource:

apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: abc-pqr-cert
spec:
  secretName: abc-pqr-tls
  dnsNames:
  - abc.pqr.com
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer


	•	Apply the certificate request:

kubectl apply -f abc-pqr-cert.yaml


	•	Option 2: Upload an Existing Certificate
	•	If you already have a certificate for abc.pqr.com, store it as a Kubernetes Secret:

kubectl create secret tls abc-pqr-tls --cert=path-to-cert.pem --key=path-to-key.pem


	•	Update the tls section of the Ingress Resource to reference this secret.

4. Test the Subdomain

	•	Once DNS records propagate (this can take a few minutes to hours), navigate to https://abc.pqr.com/ in a browser and verify that it serves the new deployment.

Coexisting with https://www.pqr.com/

If you already have an Ingress for www.pqr.com, both configurations can coexist. The Ingress controller will route traffic based on the host rules:
	•	Requests to https://www.pqr.com/ will go to your existing deployment.
	•	Requests to https://abc.pqr.com/ will go to the new deployment.

Here’s an example of a combined Ingress Resource for both:

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: combined-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - www.pqr.com
    - abc.pqr.com
    secretName: pqr-tls  # Use a wildcard or multi-domain certificate if available
  rules:
  - host: www.pqr.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: root-service
            port:
              number: 80
  - host: abc.pqr.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: abc-service
            port:
              number: 80

Optional Considerations

	1.	Wildcard Certificates:
	•	If you plan to host multiple subdomains (abc.pqr.com, xyz.pqr.com, etc.), consider using a wildcard certificate (*.pqr.com) for simplicity.
	2.	Separate Load Balancer for Subdomain (Optional):
	•	If you want more isolation, you can create a separate LoadBalancer service for the new deployment. Update the DNS A Record for abc.pqr.com to point to this new Load Balancer’s public IP.

This setup ensures both your root domain (https://www.pqr.com) and subdomain (https://abc.pqr.com) are served securely and independently from the same AKS cluster. Let me know if you’d like help with any specific step!
