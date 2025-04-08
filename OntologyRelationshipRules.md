### Object Property Characteristics (with Examples):

#### 1. **Functional**
- **Meaning:** An individual can have **at most one** value for this property.
- **Example:**  
  `hasBiologicalMother` → A person can have **only one** biological mother.
- **Effect:** If someone is linked to two different individuals via this property, a reasoner will infer those two must be the same person.

---

#### 2. **Inverse Functional**
- **Meaning:** The **object** of the property can be linked to **at most one** subject.
- **Example:**  
  `hasSSN` → If two people have the same SSN, then they are the **same individual**.
- **Effect:** Useful for uniquely identifying individuals.

---

#### 3. **Transitive**
- **Meaning:** If A is related to B, and B to C, then A is related to C.
- **Example:**  
  `isAncestorOf` → If Alice is an ancestor of Bob, and Bob of Carol, then Alice is an ancestor of Carol.
- **Effect:** Great for hierarchical or chained relationships.

---

#### 4. **Symmetric**
- **Meaning:** If A is related to B, then B is related to A.
- **Example:**  
  `isSiblingOf` → If Alice is a sibling of Bob, then Bob is a sibling of Alice.
- **Effect:** Automatically infers the reverse relationship.

---

#### 5. **Asymmetric**
- **Meaning:** If A is related to B, then B **cannot** be related to A.
- **Example:**  
  `isParentOf` → If Alice is a parent of Bob, then Bob **cannot** be a parent of Alice.
- **Note:** You cannot have a property be both symmetric and asymmetric.

---

#### 6. **Reflexive**
- **Meaning:** Every individual is related to **itself** through this property.
- **Example:**  
  `knows` → A person knows themselves.
- **Effect:** Not often used, but useful in some logic models.

---

#### 7. **Irreflexive**
- **Meaning:** No individual is related to itself via this property.
- **Example:**  
  `isTallerThan` → You cannot be taller than yourself.
- **Effect:** Helps ensure logical consistency.

---

#### 8. **Inverse Of**
- **Meaning:** You can define a property as the inverse of another.
- **Example:**  
  `hasChild` is the inverse of `isChildOf`  
  → If A `hasChild` B, then B `isChildOf` A.
- **Effect:** Helps with bidirectional querying and reasoning.

---

### *Disjoint Object Property*

Two (or more) **object properties** are **disjoint** if they can **never relate the same subject to the same object**.

### Simple Definition:
> If property **P1** and **P2** are disjoint, and individual **A** is related to **B** via **P1**, then **A cannot be related to B via P2**, and vice versa.

### Example:

Let’s say you have:
- `isParentOf`
- `isSiblingOf`

You might declare:
```
DisjointObjectProperties: isParentOf, isSiblingOf
```

Because we don't want someone to be **both** the parent and sibling of the same person.

So if in your ontology:
```
Alice isParentOf Bob
Bob isSiblingOf Alice ❌ (this would trigger a conflict!)
```

---
