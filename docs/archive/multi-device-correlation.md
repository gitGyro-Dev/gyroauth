# docs/multi-device-correlation.md

# Multi-Device Correlation Authentication

---

## 1. Purpose

This note proposes a **multi-device correlation model** for high-assurance scenarios such as:

* high-value bank transfers
* critical administrative approvals
* high-risk financial operations

The purpose is to make authentication depend not only on one device state, but on the **correlated presence of multiple devices**.

---

## 2. Core Idea

A transaction initiated on a PC should only become valid if the approving smartphone is proven to be physically near that PC.

This shifts authentication from:

* "Is the credential valid?"

to:

* "Are the required devices co-located in the same local physical context?"

---

## 3. State Model

Let:

* (X_{pc}): state of the PC
* (X_{mob}): state of the smartphone

Define:

[
X_{pc} = (I_{pc}, W_{pc}, T_{pc})
]

[
X_{mob} = (G_{mob}, W_{mob}, T_{mob}, M_{mob})
]

Where:

* (I_{pc}): PC-side network/IP-based position evidence
* (W_{pc}): Wi-Fi fingerprint around PC
* (T_{pc}): PC time context
* (G_{mob}): smartphone GPS / coarse location
* (W_{mob}): smartphone Wi-Fi fingerprint
* (T_{mob}): smartphone time context
* (M_{mob}): smartphone motion/device state

---

## 4. Correlation Objective

The system estimates whether both devices are within the same physical zone.

[
Corr(X_{pc}, X_{mob}) \geq \theta
]

If correlation is below threshold, the action is blocked.

---

## 5. Practical Approximation

Absolute proof of “same room” may be hard.

A practical implementation uses evidence fusion:

* PC public/private IP context
* overlap in Wi-Fi BSSID set
* Wi-Fi RSSI similarity
* timing consistency
* optional Bluetooth/UWB proximity if available

This yields a proximity score:

[
P_{near} = f(I_{pc}, W_{pc}, G_{mob}, W_{mob}, T)
]

---

## 6. Example Decision Rule

[
Auth = 1 \iff
\begin{cases}
score_{state} \geq \theta_1 \
P_{near} \geq \theta_2
\end{cases}
]

For example:

* (score_{state} \geq 0.85)
* (P_{near} \geq 0.90)

If PC and smartphone are not sufficiently correlated, the transfer button remains disabled.

---

## 7. Engineering Interpretation

The system does not require exact GPS agreement.

Instead, it asks:

* do these devices appear to inhabit the same local environment?
* do they observe similar radio surroundings?
* are their timestamps mutually consistent?

This is stronger than ordinary 2FA because the second factor must be **physically nearby**, not merely reachable.

---

## 8. Why This Matters

Typical high-value transaction flow:

* attacker compromises PC session
* attacker triggers transfer remotely
* victim receives approval prompt on phone

In conventional systems, that phone can approve from anywhere.

In multi-device correlation, remote approval is insufficient.

The phone must be near the originating PC environment.

---

## 9. Security Benefit

This helps block:

* remote takeover of desktop banking sessions
* approval from geographically unrelated locations
* stolen credentials plus out-of-context device approval

It introduces **distance as a logical condition**.

---

## 10. Development Considerations

### Data quality

* PC-side location is often weak
* Wi-Fi fingerprint overlap becomes highly important

### Enterprise deployment

This model works especially well when:

* corporate Wi-Fi is managed
* office/floor/room signal maps are stable
* endpoints are known devices

### Consumer deployment

For retail banking, thresholds should be more tolerant:

* "same home / same local zone" may be sufficient
* exact 5m proof may be replaced by high-confidence environmental similarity

---

## 11. Optional Enhancements

* Bluetooth handshake between PC and phone
* WebAuthn + phone proximity binding
* UWB for precise enterprise deployments
* nonce shared across both devices to bind the same transaction

---

## 12. Suggested PoC Design

### Input

* PC network and Wi-Fi environment
* smartphone GPS and Wi-Fi environment
* synchronized transaction nonce

### Output

* proximity score
* final authentication decision

### Metrics

* legitimate same-room approval rate
* remote approval rejection rate
* tolerance under noisy Wi-Fi conditions

---

## 13. Key Statement

Authentication should not only verify the user.

It should verify the **co-location of the approving devices**.

---

## 14. Conclusion

Multi-device correlation turns physical proximity into a first-class authentication variable.

In high-value workflows, this creates a much stronger form of evidence than standard multi-factor authentication.
