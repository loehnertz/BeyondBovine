# Sources

Each entry says what the source is used for and what its scope actually covers. An entry does not mean that a claim is supported. What the source justifies for this project is what matters.

**Read status** records how much of a source an agent or Jakob has actually read. Do not use a source for a consequential claim before reading enough of it to understand its scope.

## Project method

### NASA-STD-7009B, *Standard for Models and Simulations* (2024) and NASA-HDBK-7009, its implementation handbook

- **Link:** https://standards.nasa.gov/standard/NASA/NASA-STD-7009
- **Used for:** separating verification (whether the implementation follows the model) from validation (whether the model represents reality adequately for its intended use), and recording intended use, assumptions, and credibility evidence. It is cited in [decision 0002](decisions/0002-project-records.md).
- **Scope:** NASA's general practice for models and simulations. It justifies the documentation approach only. It says nothing about bioprocesses.
- **Read status:** existence and purpose confirmed from the NASA standards pages. The document itself has not been read in detail.

### Nygard, M. (2011). *Documenting Architecture Decisions*

- **Link:** https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- **Used for:** the decision-record format in `docs/decisions/`. It is cited in [decision 0002](decisions/0002-project-records.md).
- **Scope:** software architecture practice.
- **Read status:** not read in detail. The format is widely known.

## Science: candidates, not yet read

These were named in discussion as likely sources for the fed-batch question. No project claim rests on them yet.

### Sonnleitner, B. & Käppeli, O. (1986). Growth of *Saccharomyces cerevisiae* is controlled by its limited respiratory capacity: Formulation and verification of a hypothesis

- **Journal:** *Biotechnology and Bioengineering* 28(6), 927–937
- **DOI:** https://doi.org/10.1002/bit.260280620
- **Expected use:** the respiratory "bottleneck" model of yeast overflow metabolism, in which glucose is partly respired and partly converted to ethanol once the cell's respiratory capacity is exceeded.
- **Scope to check:** which strain, which operating conditions (batch, chemostat, fed-batch), and which parameter values and how they were obtained.
- **Read status:** bibliographic details and abstract confirmed. Not read.

### Doran, P. M. (2013). *Bioprocess Engineering Principles* (2nd ed.)

- **Publisher:** Academic Press
- **Expected use:** an introductory reference for mass balances, growth kinetics, fed-batch operation, and oxygen transfer.
- **Scope to check:** a general textbook. Values in its examples are illustrative unless they are traced to primary sources.
- **Read status:** not read.

### Villadsen, J., Nielsen, J. & Lidén, G. (2011). *Bioreaction Engineering Principles* (3rd ed.)

- **Publisher:** Springer
- **DOI:** https://doi.org/10.1007/978-1-4419-9688-6
- **Expected use:** a more rigorous reference for stoichiometry, kinetics, and bioreactor modelling, including fed-batch and mass transfer.
- **Scope to check:** as for Doran. Parameter values need their primary sources.
- **Read status:** not read.
