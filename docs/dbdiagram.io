// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table customers {
  id integer [primary key]
  name varchar
  email varchar
  created_at timestamp
  updated_at timestamp
  deleted_at timestamp
  wishlist_id integer
}

Table products {
  id integer [primary key]
  title varchar
  price varchar
  brand varchar
  image varchar
  review_score varchar
  created_at timestamp
  updated_at timestamp
  deleted_at timestamp
}

Table wishlists {
  id integer [primary key]
  name varchar
  created_at timestamp
  updated_at timestamp
  deleted_at timestamp
}

Table wishlist_product {
  id integer [primary key]
  name varchar
  product_id integer
  wishlist_id integer
  created_at timestamp
}

Ref: customers.wishlist_id > wishlists.id // many-to-one

Ref: wishlist_product.wishlist_id > wishlists.id // many-to-one

Ref: wishlist_product.product_id > products.id // many-to-one

