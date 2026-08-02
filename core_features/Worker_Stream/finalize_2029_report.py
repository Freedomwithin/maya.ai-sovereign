SHA256 = 2,
  CS_HASHTYPE_SHA256_TRUNCATED = 3,
  CS_HASHTYPE_SHA384 = 4,

  CS_SHA1_LEN = 20,
  CS_SHA256_LEN = 32,
  CS_SHA256_TRUNCATED_LEN = 20,

  CS_CDHASH_LEN = 20,    /* always - larger hashes are truncated */
  CS_HASH_MAX_SIZE = 48, /* max size of the hash we'll support */

  /*
   * Currently only to support Legacy VPN plugins, and Mac App Store
   * but intended to replace all the various platform code, dev code etc. bits.
   */
  CS_SIGNER_TYPE_UNKNOWN = 0,
  CS_SIGNER_TYPE_LEGACYVPN = 5,
  CS_SIGNER_TYPE_MAC_APP_STORE = 6,

  CS_SUPPL_SIGNER_TYPE_UNKNOWN = 0,
  CS_SUPPL_SIGNER_TYPE_TRUSTCACHE = 7,
  CS_SUPPL_SIGNER_TYPE_LOCAL = 8,
};

struct CS_CodeDirectory {
  uint32_t magic;         /* magic number (CSMAGIC_CODEDIRECTORY) */
  uint32_t length;        /* total length of CodeDirectory blob */
  uint32_t version;       /* compatibility version */
  uint32_t flags;         /* setup and mode flags */
  uint32_t hashOffset;    /* offset of hash slot element at index zero */
  uint32_t identOffset;   /* offset of identifier string */
  uint32_t nSpecialSlots; /* number of special hash slots */
  uint32_t nCodeSlots;    /* number of ordinary (code) hash slots */
  uint32_t codeLimit;     /* limit to main image signature range */
  uint8_t hashSize;       /* size of each hash in bytes */
  uint8_t hashType;       /* type of hash (cdHashType* constants) */
  uint8_t platform;       /* platform identifier; zero if not platform binary */
  uint8_t pageSize;       /* log2(page size in bytes); 0 => infinite */
  uint32_t spare2;        /* unused (must be zero) */

  /* Version 0x20100 */
  uint32_t scatterOffset; /* offset of optional scatter vector */

  /* Version 0x20200 */
  uint32_t teamOffset; /* offset of optional team identifier */

  /* Version 0x20300 */
  uint32_t spare3;      /* unused (must be zero) */
  uint64_t codeLimit64; /* limit to main image signature range, 64 bits */

  /* Version 0x20400 */
  uint64_t execSegBase;  /* offset of executable segment */
  uint64_t execSegLi