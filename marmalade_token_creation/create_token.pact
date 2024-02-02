;; marmalade-ng = n_442d3e11cfe0d39859878e5b1520cd8b8c36e5db
(use n_442d3e11cfe0d39859878e5b1520cd8b8c36e5db.ledger)
(use n_442d3e11cfe0d39859878e5b1520cd8b8c36e5db.std-policies)

(let
  (
      ;; Generate token id
      (token_id:string (create-token-id (read-keyset "ks-happybanana78-01") (read-string "metadata")))
  )
  
  ;; Create token
  (create-token token_id 0
      (read-string "metadata")
      (to-policies "ROYALTY INSTANT-MINT NON-FUNGIBLE")
      (read-keyset "ks-happybanana78-01")
  )

  ;; Mint token
  (mint token_id
      (read-string "owner_account")
      (read-keyset "ks-owner-happybanana78-01")
      1.0
  )
)
