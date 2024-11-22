import streamlit as st

def apply_custom_css():
    css = """
    @charset "UTF-8";

    .Mob_V {
        visibility: hidden;
    }

    .cl_1 {
        color: #acc1e6;
    }

    .cl_w {
        color: green;
    }

    .cl_d {
        color: blue;
    }

    .cl_l {
        color: red;
    }

    .cl_g {
        color: silver;
        color: #9ba6b1;
    }

    .cl_O {
        color: #919;
    }

    .ukr {
        color: #0080ff;
        color: #55F;
        color: #0808ff;
    }

    .rus {
        color: #911;
    }

    .blr {
        color: #191;
        color: #919;
    }

    .cl_PG1 {
        color: #360;
    }

    .cl_PG2 {
        color: #690;
    }

    .cl_PG3 {
        color: #906;
    }

    .cl_PG4 {
        color: #603;
    }

    .cl_n {
        color: #2f4f4f;
    }

    .cl_t {
        color: #384048;
    }

    .cl_h {
        color: #2e5498;
    }

    .fs_s {
        font-size: 0.6875rem;
    }

    .fs_b {
        font-size: 0.75rem;
    }

    .fs_nm {
        font-size: 0.75rem;
    }

    .fs_n {
        font-size: 0.8125rem;
    }

    .fs_np {
        font-size: 0.875rem;
    }

    .fs_c {
        font-size: 0.875rem;
    }

    .fs_h {
        font-size: 1rem;
    }

    .fw_n {
        font-weight: 400;
    }

    .bc {
        background: #FFF3CA;
    }

    .bc_LB {
        background: LightBlue;
    }

    .tbr {
        height: 20px;
        padding: 0;
    }

    .NBN {
        border-style: none;
    }

    .NB {
        border-style: hidden;
    }

    .NB_LR,
    .blr_h,
    .bc,
    .tbr {
        border-left-style: hidden;
        border-right-style: hidden;
    }

    .bl_h {
        border-left-style: hidden;
    }

    .bor_0 {
        border: 0;
    }

    .bor_1 {
        border: 1px solid #fffff0;
    }

    .bor_2 {
        border: 3px double #fffff0;
    }

    body {
        margin: 0;
        padding: 0;
        min-height: 1080px;
        line-height: 1.2;
        color: #384048;
        background: #e6d0ac;
        background: linear-gradient(to top, #987654, #e6d0ac);
        text-align: center;
        font-size: 0.75rem;
        font-weight: 400;
    }

    a[rel~=nofollow] {
        background: inherit !important;
        font-size: inherit !important;
    }

    .ff_n,
    body,
    .Name,
    .SN,
    .TRN,
    .EN,
    .TN,
    Caption.Line,
    th.Line,
    .btn,
    Table.Odds Caption {
        font-family: "Segoe UI", "Helvetica Neue", "Trebuchet MS", "Microsoft Sans Serif", "PT Sans", Roboto, sans-serif;
    }

    .ff_m,
    em,
    Table,
    .Mono,
    .Sel,
    .Notes,
    .Dbg,
    input {
        font-family: Consolas, Monaco, Menlo, "Lucida Console", "Courier New X", "PT Mono", "Roboto Mono", monospace, serif;
    }

    div {
        border: 1px solid #acc1e6;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
