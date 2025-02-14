"""Módulo para transformação de vazão em Energia Natural Afluente."""

import pandas as pd

from ena_ons import regras


class VazaoENA:
    """Classe para transformação vazão -> ENA."""

    def __init__(
        self,
        dados: pd.DataFrame,
        produtibilidade: pd.DataFrame,
        agrupamentos: pd.DataFrame,
        hidrograma_belo_monte: pd.DataFrame,
    ) -> None:
        """
        Inicialização da classe.

        Parameters
        ----------
        dados : pd.DataFrame
            Dataframe com postos como colunas, datas como index e valores sendo vazão.
        produtibilidade : pd.DataFrame:
            Dataframe com colunas "codigo", "produtibilidade" para todos os postos com
            valor de produtibilidade.
        agrupamentos : pd.DataFrame
            Agrupamentos desejados para agrupar valores de ENA.
        hidrograma : pd.DataFrame
            Vazões do hidrograma (médio) de Belo Monte por mês.
        """
        self.dados = dados
        self.produtibilidade = produtibilidade
        self.agrupamentos = agrupamentos
        self.hidrograma = hidrograma_belo_monte

    @staticmethod
    def calcular_artificiais_alto_tiete(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões artificiais da bacia do Alto Tietê.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Alto Tietê.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        traicao = regras.Traicao(df_pivot).calcular()
        pedreira = regras.Pedreira(df_pivot).calcular()
        billings_pedras = regras.BillingsPedras(df_pivot).calcular()
        pedras = regras.Pedras(df_pivot).calcular()
        edgard_souza = regras.EdgardSouza(df_pivot).calcular()
        henry_borden = regras.HenryBorden(df_pivot).calcular()
        billings_artificial = regras.BillingsArtificial(df_pivot).calcular()
        bbonita = regras.BarraBonitaArtificial(df_pivot).calcular()
        bariri_art = regras.BaririArtificial(df_pivot).calcular()
        ibitinga_art = regras.IbitingaArtificial(df_pivot).calcular()
        promissao_art = regras.PromissaoArtificial(df_pivot).calcular()
        navanhandava_art = regras.NovaAvanhandavaArtificial(df_pivot).calcular()
        tres_irmaos_art = regras.TresIrmaosArtificial(df_pivot).calcular()
        ilha_solteira = regras.IlhaSolteiraEquivalente(df_pivot).calcular()
        jupia_art = regras.JupiaArtificial(df_pivot).calcular()
        pprimavera_art = regras.PortoPrimaveraArtificial(df_pivot).calcular()
        itaipu_art = regras.ItaipuArtificial(df_pivot).calcular()

        df_alto_tiete = pd.concat(
            [
                traicao,
                pedreira,
                billings_pedras,
                pedras,
                edgard_souza,
                henry_borden,
                billings_artificial,
                bbonita,
                bariri_art,
                ibitinga_art,
                promissao_art,
                navanhandava_art,
                tres_irmaos_art,
                ilha_solteira,
                jupia_art,
                pprimavera_art,
                itaipu_art,
            ]
        )

        return df_alto_tiete.reset_index()

    @staticmethod
    def calcular_artificiais_paraiba_sul(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões artificiais da bacia do Paraíba do Sul.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Paraíba do Sul.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        bombeamento_sta_cecilia = regras.BombeamentoSantaCecilia(df_pivot).calcular()
        vertimento_tocos = regras.VertimentoTocos(df_pivot).calcular()
        santana_natural = regras.SantanaNatural(df_pivot).calcular()
        santana_art = regras.SantanaArtificial(df_pivot).calcular()
        vigario_art = regras.VigarioArtificial(df_pivot).calcular()
        vertimento_santana = regras.VertimentoSantana(df_pivot).calcular()
        anta_art = regras.AntaArtificial(df_pivot).calcular()
        simplicio_art = regras.SimplicioArtificial(df_pivot).calcular()
        ilha_pombos_art = regras.IlhaPombosArtificial(df_pivot).calcular()
        nilo_pecanha_art = regras.NiloPecanhaArtificial(df_pivot).calcular()
        lajes_art = regras.LajesArtificial(df_pivot).calcular()
        fontes_art = regras.FontesArtificial(df_pivot).calcular()
        pereira_passos_art = regras.PereiraPassosArtificial(df_pivot).calcular()

        df_paraiba_sul = pd.concat(
            [
                bombeamento_sta_cecilia,
                vertimento_tocos,
                santana_natural,
                santana_art,
                vigario_art,
                vertimento_santana,
                anta_art,
                simplicio_art,
                ilha_pombos_art,
                nilo_pecanha_art,
                lajes_art,
                fontes_art,
                pereira_passos_art,
            ]
        )

        return df_paraiba_sul.reset_index()

    @staticmethod
    def calcular_naturais_sao_francisco(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões naturais da bacia do São Francisco.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Naturais do São Francisco.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        pafonso = regras.PauloAfonsoNatural(df_pivot).calcular()
        complexo = regras.ComplexoNatural(df_pivot).calcular()

        df_sf = pd.concat([pafonso, complexo])

        return df_sf.reset_index()

    @staticmethod
    def calcular_artificiais_iguacu(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões artificiais da bacia do Iguaçu.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Iguaçu.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        jordao = regras.JordaoArtificial(df_pivot).calcular()
        segredo = regras.SegredoArtificial(df_pivot).calcular()

        df_iguacu = pd.concat([jordao, segredo])

        return df_iguacu.reset_index()

    @staticmethod
    def calcular_naturais_grande(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões naturais da bacia do Grande.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Naturais do Grande.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        return regras.ItutingaNatural(df_pivot).calcular().reset_index()

    @staticmethod
    def calcular_naturais_paraguai(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões naturais da bacia do Paraguai.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Naturais do Paraguai.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        return regras.ItiquiraII(df_pivot).calcular().reset_index()

    @staticmethod
    def calcular_artificiais_xingu(
        df: pd.DataFrame, hidrograma: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Gera vazões artificial da bacia do Xingu.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.
        hidrograma : pd.DataFrame
            Vazões do hidrograma (médio) de Belo Monte por mês.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Xingu.
        """
        df_pivot = df.pivot(index="data", columns="codigo", values="valor")

        belomonte = regras.BeloMonteArtificial(df_pivot, hidrograma).calcular()
        pimental_art = regras.PimentalArtificial(df_pivot, hidrograma).calcular()

        df_xingu = pd.concat([belomonte, pimental_art])

        return df_xingu.reset_index()

    def adicionar_vazoes_artificiais(self) -> pd.DataFrame:
        """
        Adiciona vazões artificiais aos dados de vazão da entrada.

        Returns
        -------
        pd.DataFrame
            Dataframe com vazão natural afluente diária por posto.
        """
        df = self.dados.copy()
        df_alto_tiete = self.calcular_artificiais_alto_tiete(df)
        df_paraiba_sul = self.calcular_artificiais_paraiba_sul(df)
        df_sf = self.calcular_naturais_sao_francisco(df)
        df_iguacu = self.calcular_artificiais_iguacu(df)
        df_grande = self.calcular_naturais_grande(df)
        df_paraguai = self.calcular_naturais_paraguai(df)
        df_xingu = self.calcular_artificiais_xingu(df, self.hidrograma)

        return pd.concat(
            [
                df,
                df_alto_tiete,
                df_paraiba_sul,
                df_sf,
                df_iguacu,
                df_grande,
                df_paraguai,
                df_xingu,
            ]
        )

    def calcular_ena(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula valores de ENA por posto.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com valores de vazão.

        Returns
        -------
        pd.DataFrame
            Dataframe com valores de ENA.
        """
        df_prod = df.merge(self.produtibilidade, on="codigo", how="left")
        df_prod["ena"] = df_prod["valor"] * df_prod["produtibilidade"]

        return df_prod[["data", "codigo", "ena"]].rename({"ena": "valor"}, axis=1)

    def agrupar(self, df: pd.DataFrame, agrupamento: str) -> pd.DataFrame:
        """
        Agrupa valores de ENA a partir de um dos agrupamentos existentes.

        Parameters
        ----------
        df : pd.DataFrame
            Valores calculados de ENA por posto.
        agrupamento : str
            Nome do agrupamento aceito [subsistemas, REE ou bacias].

        Returns
        -------
        pd.DataFrame
            ENA somada por agrupamento.
        """
        if agrupamento not in self.agrupamentos.columns:
            raise ValueError(
                "Agrupamento não existe no dataframe passado na construção da classe!"
            )

        df_relacao = df.merge(self.agrupamentos, on="codigo", how="left")

        df_agrupado = df_relacao[["data", agrupamento, "valor"]]
        df_agrupado = df_agrupado.groupby(["data", agrupamento]).sum().reset_index()

        return df_agrupado
