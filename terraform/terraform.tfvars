project     = "metar-project"

accounts    = {
    bigquery    = "roles/bigquery.admin"
    storage     = "roles/storage.admin"
    main-viewer = "roles/viewer"
    dataproc    = "roles/dataproc.admin"
  }

buckets = ["batch", "streaming"]

location = "EU"