project     = "metar-project-test"

accounts    = {
    bigquery    = "roles/bigquery.admin"
    storage     = "roles/storage.admin"
    main-viewer = "roles/viewer"
    dataproc    = "roles/dataproc.admin"
  }

buckets = ["batch", "streaming", "code", "dataproc-staging-bucket"]

location = "EU"