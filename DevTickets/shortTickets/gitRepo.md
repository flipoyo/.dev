GitRepo is a specific Graph for GX4G. cgitsync should depends on it. 

I think i need a GitRepo G that will provide the implementation of Graph and GitRepo.

cgitsync mounts GitRepo as GitTree that it protects through the never exposed interface MerkleTree (MerkleRoot Tree) that omniscience Synthesize with hash256(MerkleRoot). Therefore GX4G manages access privileges to GitRepo. It holds the GitProvider API and omniscience