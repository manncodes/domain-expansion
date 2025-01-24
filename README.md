# Domain Expansion: Parameter-Efficient Modules as Building Blocks for Composite Domains

## Abstract
Parameter-Efficient Fine-Tuning (PEFT) is an efficient alternative to full scale fine-tuning, gaining popularity recently. With pre-trained model sizes growing exponentially, PEFT can be effectively utilized to fine-tune compact modules, Parameter-Efficient Modules (PEMs), trained to be domain experts over diverse domains. In this project, we explore composing such individually fine-tuned PEMs for distribution generalization over the composite domain. To compose PEMs, simple composing functions are used that operate purely on the weight space of the individually fine-tuned PEMs, without requiring any additional fine-tuning. The proposed method is applied to the task of representing the 16 Myers-Briggs Type Indicator (MBTI) composite personalities via 4 building block dichotomies, comprising of 8 individual traits which can be merged (composed) to yield a unique personality. We evaluate the individual trait PEMs and the composed personality PEMs via an online MBTI personality quiz questionnaire, validating the efficacy of PEFT to fine-tune PEMs and merging PEMs without further fine-tuning for domain composition.

If you find this repository useful, please cite our work:

```bibtex
@misc{patel2024domain,
  title={Domain Expansion: Parameter-Efficient Modules as Building Blocks for Composite Domains},
  author={Mann Patel and Divyajyoti Panda and Hilay Mehta and Parth Patel and Dhruv Parikh},
  year={2024},
  publisher={arXiv},
  primaryClass={cs.LG},
  url={https://github.com/manncodes/domain-expansion}
}
