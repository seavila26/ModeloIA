import styled from 'styled-components';

import { v } from '../../styles/variables';

export const SLayout = styled.div`
    display: flex;
`;

export const SMain = styled.main`
    padding: calc(${v.mdSpacing} * 2) calc(${v.lgSpacing} * 2);
    //background: #00f;
    width: 100%;

    h1 {
        font-size: 24px;
    }
`;