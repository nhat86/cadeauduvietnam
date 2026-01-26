fetch("http://localhost:8000/products/")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("produits");

    data.forEach(produit => {
      const div = document.createElement("div");
      div.innerHTML = `
        <h3>${produit.name}</h3>
        <p>${produit.description || "Aucune description"}</p>
        <p>${produit.price} €</p>
      `;
      container.appendChild(div);
    });
  });
