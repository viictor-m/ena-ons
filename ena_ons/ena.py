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
        traicao = regras.Traicao(df).calcular()
        pedreira = regras.Pedreira(df).calcular()
        billings_pedras = regras.BillingsPedras(df).calcular()
        pedras = regras.Pedras(df).calcular()
        edgard_souza = regras.EdgardSouza(df).calcular()
        henry_borden = regras.HenryBorden(df).calcular()
        billings_artificial = regras.BillingsArtificial(df).calcular()
        bbonita = regras.BarraBonitaArtificial(df).calcular()
        bariri_art = regras.BaririArtificial(df).calcular()
        ibitinga_art = regras.IbitingaArtificial(df).calcular()
        promissao_art = regras.PromissaoArtificial(df).calcular()
        navanhandava_art = regras.NovaAvanhandavaArtificial(df).calcular()
        tres_irmaos_art = regras.TresIrmaosArtificial(df).calcular()
        ilha_solteira = regras.IlhaSolteiraEquivalente(df).calcular()
        jupia_art = regras.JupiaArtificial(df).calcular()
        pprimavera_art = regras.PortoPrimaveraArtificial(df).calcular()
        itaipu_art = regras.ItaipuArtificial(df).calcular()

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
            ],
            axis=1,
        )

        return df_alto_tiete

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
        bombeamento_sta_cecilia = regras.BombeamentoSantaCecilia(df).calcular()
        vertimento_tocos = regras.VertimentoTocos(df).calcular()
        santana_natural = regras.SantanaNatural(df).calcular()
        santana_art = regras.SantanaArtificial(df).calcular()
        vigario_art = regras.VigarioArtificial(df).calcular()
        vertimento_santana = regras.VertimentoSantana(df).calcular()
        anta_art = regras.AntaArtificial(df).calcular()
        simplicio_art = regras.SimplicioArtificial(df).calcular()
        ilha_pombos_art = regras.IlhaPombosArtificial(df).calcular()
        nilo_pecanha_art = regras.NiloPecanhaArtificial(df).calcular()
        lajes_art = regras.LajesArtificial(df).calcular()
        fontes_art = regras.FontesArtificial(df).calcular()
        pereira_passos_art = regras.PereiraPassosArtificial(df).calcular()

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
            ],
            axis=1,
        )

        return df_paraiba_sul

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
        pafonso = regras.PauloAfonsoNatural(df).calcular()
        complexo = regras.ComplexoNatural(df).calcular()

        df_sf = pd.concat([pafonso, complexo], axis=1)

        return df_sf

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
        jordao = regras.JordaoArtificial(df).calcular()
        segredo = regras.SegredoArtificial(df).calcular()

        df_iguacu = pd.concat([jordao, segredo], axis=1)

        return df_iguacu

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
        return regras.ItutingaNatural(df).calcular()

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
        return regras.ItiquiraII(df).calcular()

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
        belomonte = regras.BeloMonteArtificial(df, hidrograma).calcular()
        pimental_art = regras.PimentalArtificial(df, hidrograma).calcular()

        df_xingu = pd.concat([belomonte, pimental_art], axis=1)

        return df_xingu

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
            ],
            axis=1,
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
        df_melt = df.melt(
            value_name="valor", var_name="codigo", ignore_index=False
        ).reset_index()
        df_prod = df_melt.merge(self.produtibilidade, on="codigo", how="left")
        df_prod = df_prod.assign(ena=df_prod.valor * df_prod.produtibilidade)

        df_ena = df_prod[["data", "codigo", "ena"]].pivot(
            index="data", columns="codigo", values="ena"
        )
        return df_ena

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

        df_melt = df.melt(
            value_name="valor", var_name="codigo", ignore_index=False
        ).reset_index()
        df_relacao = df_melt.merge(self.agrupamentos, on="codigo", how="left")

        df_agrupado = df_relacao[["data", agrupamento, "valor"]]
        df_agrupado = df_agrupado.groupby(["data", agrupamento]).sum().reset_index()
        df_pivotado = df_agrupado.pivot(
            index="data", columns=agrupamento, values="valor"
        )

        return df_pivotado
