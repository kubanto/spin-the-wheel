
# 🎡 Spin the Wheel – Kubernetes Stateful Demo

Spin the Wheel is a **simple stateful application** designed for Kubernetes backup & restore demos (works with any Kubernetes-native backup tool, e.g. Velero or similar).

The goal is to show, *visually*, how:
- a Kubernetes application
- with **persistent storage (PVC / Longhorn)**
- can be **backed up, deleted, and restored**
- while keeping **data and behavior unchanged**.

---

## ✨ App features

- "Spin the Wheel" game with an animated graphical wheel (canvas)
- Player name entry
- 3 spins per game, with individual results shown on screen
- Final score = sum of the 3 spins
- Sound effects generated via the Web Audio API (no external audio files), with a mute button
- Confetti animation on game over
- Persistent score storage (SQLite on a PVC)
- Leaderboard sorted by score, with 🥇🥈🥉 medals for the top three

---

## 🧱 Architecture

- **Backend**: Python + Flask
- **Frontend**: vanilla HTML/CSS/JS, no external dependencies (fully self-contained)
- **Database**: SQLite
- **Storage**: PVC (Longhorn)
- **Container runtime**: containerd
- **Exposure**: NodePort Service (fixed port)

---

## 📂 Repository structure

```
spin-the-wheel/
├── app.py
├── Dockerfile
├── requirements.txt
├── static/
│   └── index.html
├── k8s/
│   ├── 00-namespace.yaml
│   ├── 10-pvc.yaml
│   ├── 20-deployment.yaml
│   └── 30-service.yaml
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🚀 Building the image

The image must be built directly on the node where the pod will run (the Deployment uses `imagePullPolicy: Never`, so it never pulls from a registry) and imported into containerd's `k8s.io` namespace, the one kubelet queries via CRI.

**On k3s:**
```bash
export CONTAINERD_ADDRESS=/run/k3s/containerd/containerd.sock
export CONTAINERD_NAMESPACE=k8s.io

sudo nerdctl build -t spin-the-wheel:1.0 .
```

**On a "vanilla" kubeadm cluster with standard containerd** (socket at `/run/containerd/containerd.sock`, no need to install Docker):
```bash
# nerdctl + buildkit, if not already present
curl -sSL https://github.com/containerd/nerdctl/releases/download/v2.0.5/nerdctl-full-2.0.5-linux-<arch>.tar.gz -o nerdctl-full.tar.gz
sudo tar Cxzvf /usr/local nerdctl-full.tar.gz
sudo systemctl enable --now buildkit

sudo nerdctl --namespace k8s.io build -t spin-the-wheel:1.0 .
sudo nerdctl --namespace k8s.io images | grep spin-the-wheel
```
(replace `<arch>` with `amd64` or `arm64` depending on the node)

To update the app after a change: rebuild with the same tag, then
```bash
kubectl rollout restart deployment/spin-the-wheel -n spin-the-wheel
```

---

## ☸️ Deploying to Kubernetes

```bash
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/10-pvc.yaml
kubectl apply -f k8s/20-deployment.yaml
kubectl apply -f k8s/30-service.yaml
```

---

## 🌍 Accessing the app

```text
http://<NODE-IP>:31080
```

---

## 💾 Backup & Restore demo

1. Create a backup policy for the `spin-the-wheel` namespace using your Kubernetes backup tool of choice
2. Run a backup
3. Simulate a disaster:
   ```bash
   kubectl delete ns spin-the-wheel
   ```
4. Restore from the backup
5. Verify that the leaderboard is unchanged

---

## 🎯 Why this makes a good demo

- **Visible** application state
- Real persistent storage
- Immediately verifiable restore
- No external dependencies

---

## ⚠️ Disclaimer

This project was created as a simple application for practicing and testing backup and restore workflows in Kubernetes environments — it is not intended for production use.

The software is provided "as is", without any express or implied warranty. Use is entirely at the user's own risk: the author assumes no liability for any damages, data loss, or malfunctions arising from the use of this project.

---

## 📜 License

MIT
