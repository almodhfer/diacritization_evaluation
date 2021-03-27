This package calculates Diacritization Error Rate (DER),
and Word Error Rate (WER) for the diacritization problem of the Arabic
language Either from paths or from texts

To install:

```
pip install diacritization_evaluation
```
Each evaluation can be calculated either with case-ending or without
case-ending. With case_ending the last character of each word is counted,
while without case_ending the last character of each word is not
counted.


```python
from diacritization_evaluation import wer, der

original_path = "path/to/original_path"
predicted_path  = "path/to/predicted_path"
use_case_ending = True

der.calculate_from_path(original_path, predicted_path, use_case_ending=use_case_ending)
wer.calculate_from_path(original_path, predicted_path, use_case_ending=use_case_ending)

```

There is another option to calculate DER, and WER directly from text.

```python
from diacritization_evaluation import wer, der
original_text = "Arabic diacritizated Text"
predicted_text = "Predicted diacritizated Text"
use_case_ending = True
der.calculate_der(original_path, predicted_path, use_case_ending=use_case_ending)
wer.calculate_wer(original_path, predicted_path, use_case_ending=use_case_ending)
```
