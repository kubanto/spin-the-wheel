
# 🎡 Spin the Wheel – Kubernetes Stateful Demo

Spin the Wheel è una **semplice applicazione stateful** pensata per demo Kubernetes e **Veeam Kasten**.

L’obiettivo è mostrare in modo *visivo* come:
- un’applicazione Kubernetes
- con **storage persistente (PVC / Longhorn)**
- possa essere **backuppata, cancellata e ripristinata**
- mantenendo **dati e comportamento invariati**.

---

## ✨ Funzionalità dell’app

- Gioco "Spin the Wheel" con ruota grafica animata (canvas)
- Inserimento nome giocatore
- 3 spin per partita, con storico dei singoli risultati mostrato a schermo
- Punteggio finale = somma dei 3 spin
- Effetti sonori generati via Web Audio API (nessun file audio esterno), con pulsante mute
- Confetti animati a fine partita
- Salvataggio persistente del risultato (SQLite su PVC)
- Leaderboard ordinata per punteggio, con medaglie 🥇🥈🥉 per i primi tre
- Interfaccia in inglese

---

## 🧱 Architettura

- **Backend**: Python + Flask
- **Frontend**: HTML/CSS/JS vanilla, nessuna dipendenza esterna (self-contained)
- **Database**: SQLite
- **Storage**: PVC (Longhorn)
- **Container runtime**: containerd
- **Exposure**: Service NodePort (porta fissa)

---

## 📂 Struttura del repository

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

## 🚀 Build dell’immagine

L'immagine va costruita direttamente sul nodo dove girerà il pod (il Deployment usa `imagePullPolicy: Never`, quindi non tira da nessun registry) e va importata nel namespace containerd `k8s.io`, quello che il kubelet consulta via CRI.

**Su k3s:**
```bash
export CONTAINERD_ADDRESS=/run/k3s/containerd/containerd.sock
export CONTAINERD_NAMESPACE=k8s.io

sudo nerdctl build -t spin-the-wheel:1.0 .
```

**Su un cluster kubeadm "vanilla" con containerd standard** (socket in `/run/containerd/containerd.sock`, non serve installare Docker):
```bash
# nerdctl + buildkit, se non già presenti
curl -sSL https://github.com/containerd/nerdctl/releases/download/v2.0.5/nerdctl-full-2.0.5-linux-<arch>.tar.gz -o nerdctl-full.tar.gz
sudo tar Cxzvf /usr/local nerdctl-full.tar.gz
sudo systemctl enable --now buildkit

sudo nerdctl --namespace k8s.io build -t spin-the-wheel:1.0 .
sudo nerdctl --namespace k8s.io images | grep spin-the-wheel
```
(sostituisci `<arch>` con `amd64` o `arm64` a seconda del nodo)

Per aggiornare l'app dopo una modifica: ribuilda con lo stesso tag, poi
```bash
kubectl rollout restart deployment/spin-the-wheel -n spin-the-wheel
```

---

## ☸️ Deploy su Kubernetes

```bash
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/10-pvc.yaml
kubectl apply -f k8s/20-deployment.yaml
kubectl apply -f k8s/30-service.yaml
```

---

## 🌍 Accesso all’app

```text
http://<NODE-IP>:31080
```

---

## 💾 Demo Backup & Restore con Veeam Kasten

1. Creare una policy Kasten sul namespace `spin-the-wheel`
2. Eseguire un backup
3. Simulare un disastro:
   ```bash
   kubectl delete ns spin-the-wheel
   ```
4. Eseguire il restore dal backup
5. Verificare che la leaderboard sia invariata

---

## 🎯 Perché è una demo efficace

- Stato applicativo **visibile**
- Storage persistente reale
- Restore immediatamente verificabile
- Nessuna dipendenza esterna

---

## ⚠️ Disclaimer

Questo progetto è stato pensato come una semplice applicazione per fare pratica e test di backup e restore in ambienti Kubernetes — non è destinato a un uso in produzione.

Il software è fornito "così com'è", senza alcuna garanzia esplicita o implicita. L'uso è a totale responsabilità di chi lo utilizza: l'autore non si assume alcuna responsabilità per eventuali danni, perdita di dati o malfunzionamenti derivanti dall'uso di questo progetto.

---

## 📜 Licenza

MIT
