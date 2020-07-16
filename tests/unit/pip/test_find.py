import sys

import pytest

import light_the_torch as ltt
from light_the_torch import computation_backend as cb
from light_the_torch._pip.common import InternalLTTError
from light_the_torch._pip.find import PytorchCandidatePreferences


def test_find_links_internal_error(mocker):
    mocker.patch("light_the_torch._pip.find.extract_dists", return_value=[])
    mocker.patch("light_the_torch._pip.find.run")

    with pytest.raises(InternalLTTError):
        ltt.find_links(["foo"])


def test_PytorchCandidatePreferences_detect_computation_backend(mocker):
    class GenericComputationBackend(cb.ComputationBackend):
        @property
        def local_specifier(self):
            return "generic"

    computation_backend = GenericComputationBackend()
    mocker.patch(
        "light_the_torch._pip.find.detect_computation_backend",
        return_value=computation_backend,
    )

    candidate_prefs = PytorchCandidatePreferences()
    assert candidate_prefs.computation_backend is computation_backend


@pytest.fixture
def computation_backends():
    strings = ["cpu"]
    if sys.platform.startswith("linux") or sys.platform.startswith("win"):
        strings.extend(("cu92", "cu101", "cu102"))
    return [cb.ComputationBackend.from_str(string) for string in strings]


@pytest.mark.slow
def test_find_links_torch_smoke(subtests, computation_backends):
    dist = "torch"

    for computation_backend in computation_backends:
        with subtests.test(computation_backend=computation_backend):
            assert ltt.find_links([dist], computation_backend=computation_backend)


@pytest.mark.slow
@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="torchaudio has no releases for Windows"
)
def test_find_links_torchaudio_smoke(subtests, computation_backends):
    dist = "torchaudio"

    for computation_backend in computation_backends:
        with subtests.test(computation_backend=computation_backend):
            assert ltt.find_links([dist], computation_backend=computation_backend)


@pytest.mark.slow
def test_find_links_torchtext_smoke(subtests, computation_backends):
    dist = "torchtext"

    for computation_backend in computation_backends:
        with subtests.test(computation_backend=computation_backend):
            assert ltt.find_links([dist], computation_backend=computation_backend)


@pytest.mark.slow
def test_find_links_torchvision_smoke(subtests, computation_backends):
    dist = "torchvision"

    for computation_backend in computation_backends:
        with subtests.test(computation_backend=computation_backend):
            assert ltt.find_links([dist], computation_backend=computation_backend)
