# Einrichtung: Analysepakete und R-Kernel für Jupyter installieren.
# Installiert in die persönliche Bibliothek, dafür sind keine Adminrechte nötig.

bibliothek <- Sys.getenv("R_LIBS_USER")
dir.create(bibliothek, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(bibliothek, .libPaths()))

pakete <- c("IRkernel", "stm", "quanteda", "udpipe", "readr", "dplyr", "ggplot2")
fehlend <- pakete[!pakete %in% rownames(installed.packages())]
if (length(fehlend) > 0) {
  cat("Installiere:", paste(fehlend, collapse = ", "), "\n")
  install.packages(fehlend, lib = bibliothek, repos = "https://cloud.r-project.org")
}

# R-Kernel für Jupyter registrieren
IRkernel::installspec(user = TRUE, name = "ir", displayname = "R (bildungsbericht)")

cat("\n", R.version.string, "\n")
for (p in pakete) {
  cat(sprintf("%-10s %s\n", p, as.character(packageVersion(p))))
}