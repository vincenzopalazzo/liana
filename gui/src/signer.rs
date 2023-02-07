pub use liana::signer::SignerError;

use liana::{
    miniscript::bitcoin::{
        secp256k1,
        util::{
            bip32::{DerivationPath, ExtendedPubKey, Fingerprint},
            psbt::Psbt,
        },
        Network,
    },
    signer::HotSigner,
};

pub struct Signer {
    curve: secp256k1::Secp256k1<secp256k1::SignOnly>,
    key: HotSigner,
    fingerprint: Fingerprint,
}

impl Signer {
    pub fn new(key: HotSigner) -> Self {
        let curve = secp256k1::Secp256k1::signing_only();
        let fingerprint = key.fingerprint(&curve);
        Self {
            key,
            curve,
            fingerprint,
        }
    }

    pub fn generate(network: Network) -> Result<Self, SignerError> {
        Ok(Self::new(HotSigner::generate(network)?))
    }

    pub fn fingerprint(&self) -> Fingerprint {
        self.fingerprint
    }

    pub fn get_extended_pubkey(&self, path: &DerivationPath) -> ExtendedPubKey {
        self.key.xpub_at(path, &self.curve)
    }

    pub fn sign_psbt(&self, psbt: Psbt) -> Result<Psbt, SignerError> {
        self.key.sign_psbt(psbt, &self.curve)
    }

    pub fn store(
        &self,
        datadir_root: &std::path::Path,
        network: Network,
    ) -> Result<(), SignerError> {
        self.key.store(datadir_root, network, &self.curve)
    }
}
