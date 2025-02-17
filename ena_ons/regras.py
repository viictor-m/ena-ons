"""Módulo para tratar regras específicas para cáculo de ENA."""

import pandas as pd

from ena_ons.codigos import codigos


class Traicao:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Traição.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Traição.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.guarapiranga + self.billings
        vazao.name = codigos.traicao

        return vazao


class Pedreira:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Pedreira.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Pedreira.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.billings
        vazao.name = codigos.pedreira

        return vazao


class BillingsPedras:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Billings + Pedras.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Billings + Pedras.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (self.billings - 0.185) / 0.8103
        vazao.name = codigos.billings_pedras

        return vazao


class Pedras:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Pedras.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.billings = df[codigos.billings]
        self.billings_pedras = BillingsPedras(df).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Pedras.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.billings_pedras - self.billings
        vazao.name = codigos.pedras

        return vazao


class EdgardSouza:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Edgar de Souza s/ contribuição.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Edgar de Souza s/ contribuição.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.esouza - self.guarapiranga - self.billings
        vazao.name = codigos.edgard_souza_sem_tributarios

        return vazao


class HenryBorden:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Henry Borden Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.pedras = Pedras(df).calcular()
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Henry Borden Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.pedras
            + 0.1 * (self.esouza - self.guarapiranga - self.billings)
            + self.guarapiranga
            + self.billings
        )
        vazao.name = codigos.henry_borden

        return vazao


class BillingsArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Billings Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Billings Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            0.1 * (self.esouza - self.guarapiranga - self.billings)
            + self.guarapiranga
            + self.billings
        )
        vazao.name = codigos.billings_artificial

        return vazao


class BarraBonitaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Barra Bonita Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.barra_bonita = df[codigos.barra_bonita]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Barra Bonita Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.barra_bonita
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.barra_bonita_artificial

        return vazao


class BaririArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Bariri Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.bariri = df[codigos.bariri]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Bariri Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.bariri
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.bariri_artificial

        return vazao


class IbitingaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Ibitinga Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.ibitinga = df[codigos.ibitinga]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Ibitinga Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.ibitinga
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.ibitinga_artificial

        return vazao


class PromissaoArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Promissão Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.promissao = df[codigos.promissao]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Promissão Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.promissao
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.promissao_artificial

        return vazao


class NovaAvanhandavaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Nova Avanhandava Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.nova_avanhandava = df[codigos.nova_avanhandava]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Nova Avanhandava Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.nova_avanhandava
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.nova_avanhandava_artificial

        return vazao


class TresIrmaosArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Três Irmãos Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.tres_irmaos = df[codigos.tres_irmaos]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Três Irmãos Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.tres_irmaos
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.tres_irmaos_artificial

        return vazao


class IlhaSolteiraEquivalente:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Ilha Solteira Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.tres_irmaos = df[codigos.tres_irmaos]
        self.ilha_solteira = df[codigos.ilha_solteira]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Ilha Solteira Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            (self.tres_irmaos + self.ilha_solteira)
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.ilha_solteira_equiv

        return vazao


class JupiaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Jupiá Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.jupia = df[codigos.jupia]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Jupiá Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.jupia
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.jupia_artificial

        return vazao


class PortoPrimaveraArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Porto Primavera Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.porto_primavera = df[codigos.porto_primavera]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Porto Primavera Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.porto_primavera
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.porto_primavera_artificial

        return vazao


class ItaipuArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Itaipu Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.itaipu = df[codigos.itaipu]
        self.esouza = df[codigos.edgard_souza_com_tributarios]
        self.guarapiranga = df[codigos.guarapiranga]
        self.billings = df[codigos.billings]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Itaipu Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.itaipu
            - 0.1 * (self.esouza - self.guarapiranga - self.billings)
            - self.guarapiranga
            - self.billings
        )
        vazao.name = codigos.itaipu_artificial

        return vazao


class BombeamentoSantaCecilia:
    """Regra de cálculo de usina artificial."""

    def __init__(
        self,
        df: pd.DataFrame,
        limite_inferior: int = 190,
        limite_intermediario: int = 205,
        limite_superior: int = 250,
    ) -> None:
        """
        Regra de cálculo para Bombeamento de Santa Cecília, no Paraíba do Sul.

        Os valores dos limites se encontram no documento "Atualização de Séries
        Históricas de Vazões" mais atualizado. Este pode ser encontrado no
        SINtegre, em Programação da Operação > Acompanhamento e Previsão
        Hidrológica > Séries Históricas de Vazões Naturais.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        limite_inferior : int, optional
            Limite do intervalo inferior de vazão, by default 190
        limite_intermediario : int, optional
            Limite do intervalo intermediário, by default 205
        limite_superior : int, optional
            Limite do intervalo superior, by default 250
        """
        self.santa_cecilia = df[codigos.santa_cecilia]
        self.limite_inferior = limite_inferior
        self.limite_intermediario = limite_intermediario
        self.limite_superior = limite_superior

    def bombear(self, vazao: float) -> float:
        """
        Calcula a vazão do Bombeamento ocorrido em Santa Cecília.

        Parameters
        ----------
        vazao : float
            Valor da vazão em Santa Cecília.

        Returns
        -------
        float
            Vazão bombeada.
        """
        if vazao <= self.limite_inferior:
            nova_vazao = (vazao * 119) / 190
        elif self.limite_inferior < vazao <= self.limite_intermediario:
            nova_vazao = 119
        elif self.limite_intermediario < vazao <= self.limite_superior:
            nova_vazao = vazao - 90
        else:
            nova_vazao = 160

        return nova_vazao

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo do Bombeamento de Santa Cecília.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.santa_cecilia.apply(self.bombear)
        vazao.name = codigos.bombeamento_santa_cecilia

        return vazao


class VertimentoTocos:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para o vertimento de Tocos.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.tocos = df[codigos.tocos]

    def verter(self, vazao: float) -> float:
        """
        Define o valor da vazão vertida.

        Parameters
        ----------
        vazao : float
            Vazão de Tocos.

        Returns
        -------
        float
            Valor de vazão vertida.
        """
        return max(0, vazao - 25)

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de vertimento de Tocos.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.tocos.apply(self.verter)
        vazao.name = codigos.vertimento_tocos

        return vazao


class SantanaNatural:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para a vazão natural de Santana.

        Fator de ajuste retirado das correlações diárias, encontradas na planilha
        Regressoes_PMO, dentro do produto Dados Gerais do Processo de Previsão
        de Vazões.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.tocos = df[codigos.tocos]
        self.lajes = df[codigos.lajes]
        self.fator = 0.997

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo da vazão natural de Santana.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (self.tocos + self.lajes) * self.fator
        vazao.name = codigos.santana

        return vazao


class SantanaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Santana Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.santana = SantanaNatural(df).calcular()
        self.tocos = df[codigos.tocos]
        self.vertimento_tocos = VertimentoTocos(df).calcular()
        self.bombeamento_santa_cecilia = BombeamentoSantaCecilia(df).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Santana Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            (self.santana - self.tocos)
            + self.vertimento_tocos
            + self.bombeamento_santa_cecilia
        )
        vazao.name = codigos.santana_artificial

        return vazao


class VigarioArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Vigário Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.santana_artificial = SantanaArtificial(df).calcular()
        self.limite = 190

    def escolher(self, vazao: float) -> float:
        """
        Escolhe o valor mínimo de vazão entre o posto Santana e o limite mínimo.

        Parameters
        ----------
        vazao : float
            Valor de vazão de Santana

        Returns
        -------
        float
            Valor escolhido.
        """
        return min(vazao, self.limite)

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Vigário Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.santana_artificial.apply(self.escolher)
        vazao.name = codigos.vigario

        return vazao


class VertimentoSantana:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Vertimento de Santana.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.santana_artificial = SantanaArtificial(df).calcular()
        self.vigario_artificial = VigarioArtificial(df).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo do Vertimento de Santana.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.santana_artificial - self.vigario_artificial
        vazao.name = codigos.santana_vertimento

        return vazao


class AntaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Anta Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.anta = df[codigos.anta]
        self.bombeamento_santa_cecilia = BombeamentoSantaCecilia(df).calcular()
        self.santana = SantanaNatural(df).calcular()
        self.vertimento_santana = VertimentoSantana(df).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Anta Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.anta
            - self.bombeamento_santa_cecilia
            - self.santana
            + self.vertimento_santana
        )
        vazao.name = codigos.anta_artificial

        return vazao


class SimplicioArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(
        self,
        df: pd.DataFrame,
        limite: int = 430,
    ) -> None:
        """
        Regra de cálculo para vazão artificial de Simplício, no Paraíba do Sul.

        Os valores dos limites se encontram no documento "Atualização de Séries
        Históricas de Vazões" mais atualizado. Este pode ser encontrado no
        SINtegre, em Programação da Operação > Acompanhamento e Previsão
        Hidrológica > Séries Históricas de Vazões Naturais.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        limite : int
            Limite do intervalo de vazão, by default 430
        """
        self.anta = AntaArtificial(df).calcular()
        self.limite = limite

    def escolher(self, vazao: float) -> float:
        """
        Calcula a vazão artificial de Simplício.

        Parameters
        ----------
        vazao : float
            Valor da vazão em Santa Cecília.

        Returns
        -------
        float
            Vazão bombeada.
        """
        if vazao <= self.limite:
            nova_vazao = max(0, vazao - 90)
        else:
            nova_vazao = 340

        return nova_vazao

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Simplício Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.anta.apply(self.escolher)
        vazao.name = codigos.simplicio_artificial

        return vazao


class IlhaPombosArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Ilha dos Pombos Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.ilha_pombos = df[codigos.ilha_pombos]
        self.bombeamento_santa_cecila = BombeamentoSantaCecilia(df).calcular()
        self.santana = SantanaNatural(df).calcular()
        self.vertimento_santana = VertimentoSantana(df).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Ilha dos Pombos Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = (
            self.ilha_pombos
            - self.bombeamento_santa_cecila
            - self.santana
            + self.vertimento_santana
        )
        vazao.name = codigos.ilha_pombos_artificial

        return vazao


class NiloPecanhaArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Nilo Peçanha Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.vigario_artificial = VigarioArtificial(df).calcular()
        self.limite = 144

    def escolher(self, vazao: float) -> float:
        """
        Escolhe o valor mínimo de vazão entre o Vigário Artificial e o limite mínimo.

        Parameters
        ----------
        vazao : float
            Valor de vazão de Santana

        Returns
        -------
        float
            Valor escolhido.
        """
        return min(vazao, self.limite)

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Nilo Peçanha Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.vigario_artificial.apply(self.escolher)
        vazao.name = codigos.nilo_pecanha_artificial

        return vazao


class LajesArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Lajes Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.tocos = df[codigos.tocos]
        self.lajes = df[codigos.lajes]
        self.limite = 25

    def escolher(self, tocos: float, lajes: float) -> float:
        """
        Escolhe o valor mínimo de vazão entre o Vigário Artificial e o limite mínimo.

        Parameters
        ----------
        tocos : float
            Valor de vazão de Tocos.
        Lajes : float
            Valor de vazão de Lajes.

        Returns
        -------
        float
            Valor escolhido.
        """
        return lajes + min(tocos, self.limite)

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Lajes Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = list()
        for lajes, tocos in zip(self.lajes, self.tocos):
            valor = self.escolher(tocos, lajes)
            vazao.append(valor)

        serie = pd.Series(vazao, index=self.lajes.index)
        serie.name = codigos.lajes_artificial

        return serie


class FontesArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Fontes Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.lajes = LajesArtificial(df).calcular()
        self.vigario_artificial = VigarioArtificial(df).calcular()
        self.nilo_pecanha_artificial = NiloPecanhaArtificial(df).calcular()
        self.limite = 17

    def escolher(self, lajes: float, vigario: float, nilo_pecanha: float) -> float:
        """
        Escolhe o valor mínimo de vazão entre o Fontes Artificial e o limite mínimo.

        Parameters
        ----------
        tocos : float
            Valor de vazão de Tocos.
        Lajes : float
            Valor de vazão de Lajes.
        nilo_pecanha : float
            Valor de vazão de Nilo Peçanha.

        Returns
        -------
        float
            Valor escolhido.
        """
        if lajes < self.limite:
            nova_vazao = lajes
        else:
            nova_vazao = self.limite + min(vigario - nilo_pecanha, 34)

        return nova_vazao

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Fontes Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = list()
        for lajes, vigario_artificial, nilo_pecanha in zip(
            self.lajes, self.vigario_artificial, self.nilo_pecanha_artificial
        ):
            valor = self.escolher(lajes, vigario_artificial, nilo_pecanha)
            vazao.append(valor)

        serie = pd.Series(vazao, index=self.lajes.index)
        serie.name = codigos.fontes_artificial

        return serie


class PereiraPassosArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Pereira Passos Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.fontes = FontesArtificial(df).calcular()
        self.nilo_pecanha_artificial = NiloPecanhaArtificial(df).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Pereira Passos Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.fontes + self.nilo_pecanha_artificial
        vazao.name = codigos.pereira_passos_artificial

        return vazao


class ItutingaNatural:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Itutinga Natural.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.camargos = df[codigos.camargos]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Itutinga Natural.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.camargos.copy()
        vazao.name = codigos.itutinga

        return vazao


class PauloAfonsoNatural:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Paulo Afonso.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.moxoto = df[codigos.moxoto]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Paulo Afonso.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.moxoto.copy()
        vazao.name = codigos.paulo_afonso

        return vazao


class ComplexoNatural:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Complexo.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.moxoto = df[codigos.moxoto]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Complexo.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.moxoto.copy()
        vazao.name = codigos.complexo

        return vazao


class JordaoArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para a Artificial de Jordão.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.jordao = df[codigos.jordao]
        self.limite = 173.5

    def desviar(self, vazao: float) -> float:
        """
        Define o valor da vazão desviada.

        Parameters
        ----------
        vazao : float
            Vazão de Tocos.

        Returns
        -------
        float
            Valor de vazão vertida.
        """
        return vazao - min(self.limite, vazao - 10)

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo da artificial de Jordão.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.jordao.apply(self.desviar)
        vazao.name = codigos.jordao_artificial

        return vazao


class SegredoArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para a Artificial de Segredo.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.segredo = df[codigos.segredo]
        self.jordao = df[codigos.jordao]
        self.limite = 173.5

    def desviar(self, jordao: float, segredo: float) -> float:
        """
        Define o valor da vazão desviada.

        Parameters
        ----------
        jordao : float
            Vazão de Jordão.
        segredo : float
            Vazão de Segredo.

        Returns
        -------
        float
            Valor de vazão vertida.
        """
        desvio: float = segredo + min(jordao - 10, self.limite)
        return desvio

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Segredo Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        segredo_art = list()
        for jordao, segredo in zip(self.jordao, self.segredo):
            segredo_art.append(self.desviar(jordao, segredo))

        vazao = pd.Series(segredo_art, index=self.segredo.index)
        vazao.name = codigos.segredo_artificial

        return vazao


class ItiquiraII:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Itiquira II.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        """
        self.itiquira1 = df[codigos.itiquira1]

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Itiquira II.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.itiquira1.copy()
        vazao.name = codigos.itiquira2

        return vazao


class BeloMonteArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame, hidrograma: pd.DataFrame) -> None:
        """
        Regra de Cálculo para vazão artificial de Belo Monte.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        hidrograma : pd.DataFrame
            Vazões do hidrograma (médio) de Belo Monte por mês.
        """
        self.pimental = pd.DataFrame(df[codigos.pimental]).rename(
            {288: "pimental"}, axis=1
        )
        self.desvio_maximo = 13900
        self.hidrograma = hidrograma

    def preparar(self) -> pd.DataFrame:
        """
        Prepara os dados para o cálculo do desvio.

        Essa função junta os valores de vazão de pimental com os valores do hidrograma
        referentes ao mês da medição.

        Returns
        -------
        pd.DataFrame
            Dataframe contendo vazão de pimental e valores do hidrograma.
        """
        df = self.pimental.copy()
        idx = df.index

        df["mes"] = df.index.month  # type: ignore
        df = df.merge(self.hidrograma, how="left", on="mes")
        df = df.rename({"vazao": "hidrograma"}, axis=1)
        df.index = idx

        return df[["pimental", "hidrograma"]]

    def desviar(self, pimental: float, hidrograma: float) -> float:
        """
        Cálcula o desvio de água entre os reservatórios de Pimental e Belo Monte.

        Parameters
        ----------
        pimental : float
            Vazão no posto de Pimental
        hidrograma : float
            Valor limite do hidrograma médio

        Returns
        -------
        float
            Vazão desviada.
        """
        if pimental < hidrograma:
            vazao_desviada = 0.0
        elif pimental > hidrograma + self.desvio_maximo:
            vazao_desviada = self.desvio_maximo
        else:
            vazao_desviada = pimental - hidrograma

        return vazao_desviada

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo da artificial de Belo Monte.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        df = self.preparar()
        belomonte = list()
        for row in df.itertuples():
            belomonte.append(self.desviar(row.pimental, row.hidrograma))  # type: ignore

        vazao = pd.Series(belomonte, index=self.pimental.index)
        vazao.name = codigos.belo_monte_artificial

        return vazao


class PimentalArtificial:
    """Regra de cálculo de usina artificial."""

    def __init__(self, df: pd.DataFrame, hidrograma: pd.DataFrame) -> None:
        """
        Regra de Cálculo para Pimental Artificial.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com série diária de valores de vazão.
        hidrograma : pd.DataFrame
            Vazões do hidrograma (médio) de Belo Monte por mês.
        """
        self.pimental = df[codigos.pimental]
        self.belo_monte = BeloMonteArtificial(df, hidrograma).calcular()

    def calcular(self) -> pd.Series:
        """
        Aplica regra de cálculo de Pimental Artificial.

        Returns
        -------
        pd.Series
            Valores de vazão com regra de cálculo.
        """
        vazao = self.pimental - self.belo_monte
        vazao.name = codigos.pimental_artificial

        return vazao
